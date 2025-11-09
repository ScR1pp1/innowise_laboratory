from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            db_obj: Optional[ModelType] = None,
            id: Optional[int] = None,
            owner_id: Optional[int] = None,
            **filters
    ) -> Optional[ModelType]:
        if db_obj is None:
            if id is None:
                raise ValueError("Either db_obj or id must be provided")

            query = select(self.model).where(self.model.id == id)

            if owner_id is not None and hasattr(self.model, 'owner_id'):
                query = query.where(self.model.owner_id == owner_id)

            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

            result = await db.execute(query)
            db_obj = result.scalar_one_or_none()

            if db_obj is None:
                return None

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)

        if hasattr(db_obj, 'updated_at'):
            from datetime import datetime
            setattr(db_obj, 'updated_at', datetime.utcnow())

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj
from datetime import datetime
from typing import List, Optional, Union, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.crud.base import CRUDBase
from src.models import Account
from src.models.main import TransactionType
from src.models.tag import Tag
from src.models.transaction import Transaction
from src.schemas.transaction import TransactionCreate, TransactionUpdate
from datetime import datetime


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_multi_by_owner(self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Transaction]:
        result = await db.execute(
            select(Transaction)
            .where(
                Transaction.owner_id == owner_id,
                Transaction.is_deleted == False
            )
            .options(
                selectinload(Transaction.tags),
                selectinload(Transaction.category),
                selectinload(Transaction.account)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_owner(self, db: AsyncSession, *, obj_in: TransactionCreate, owner_id: int) -> Transaction:
        obj_in_data = obj_in.model_dump()
        db_obj = Transaction(**obj_in_data, owner_id=owner_id)

        account = await db.get(Account, obj_in.account_id)
        if obj_in.type == TransactionType.INCOME:
            account.balance += obj_in.amount
        else:
            account.balance -= obj_in.amount

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_owner(self, db: AsyncSession, *, id: int, owner_id: int) -> Optional[Transaction]:
        result = await db.execute(
            select(Transaction)
            .where(
                Transaction.id == id,
                Transaction.owner_id == owner_id,
                Transaction.is_deleted==False
            )
            .options(
                selectinload(Transaction.tags),
                selectinload(Transaction.category),
                selectinload(Transaction.account)
            )
        )
        return result.scalar_one_or_none()

    async def update(self,db: AsyncSession,*,obj_in: Union[TransactionUpdate, Dict[str, Any]], db_obj: Optional[Transaction] = None,
                     id: Optional[int] = None, owner_id: Optional[int] = None, **filters) -> Optional[Transaction]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        tag_ids = update_data.pop("tag_ids", None)

        transaction = await super().update(db, obj_in=update_data, db_obj=db_obj, id=id, owner_id=owner_id, **filters)

        if transaction and tag_ids is not None:
            transaction.tags.clear()
            if tag_ids:
                result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
                transaction.tags.extend(result.scalars().all())

            await db.commit()
            await db.refresh(transaction)

        return transaction

    async def soft_delete(self, db: AsyncSession, *, id: int, owner_id: int) -> Optional[Transaction]:
        transaction = await self.get_by_owner(db, id=id, owner_id=owner_id)
        if transaction:
            transaction.is_deleted = True
            await db.commit()
            await db.refresh(transaction)
        return transaction



    async def get_transactions_by_period(self, db: AsyncSession, *, owner_id: int, start_date: datetime, end_date: datetime) -> List[Transaction]:
        result = await db.execute(
            select(Transaction)
            .where(
                Transaction.owner_id == owner_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
                Transaction.is_deleted == False,
            )
            .options(
                selectinload(Transaction.tags),
                selectinload(Transaction.category),
            )
        )
        return result.scalars().all()

    async def get_filtered_by_owner(
        self,
        db: AsyncSession,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ) -> List[Transaction]:
        query = (
            select(Transaction)
            .where(
                Transaction.owner_id == owner_id,
                Transaction.is_deleted == False,
            )
            .options(
                selectinload(Transaction.tags),
                selectinload(Transaction.category),
                selectinload(Transaction.account),
            )
            .offset(skip)
            .limit(limit)
        )

        if start_date is not None:
            query = query.where(Transaction.date >= start_date)
        if end_date is not None:
            query = query.where(Transaction.date <= end_date)
        if type is not None:
            query = query.where(Transaction.type == type)
        if category_id is not None:
            query = query.where(Transaction.category_id == category_id)
        if account_id is not None:
            query = query.where(Transaction.account_id == account_id)

        result = await db.execute(query)
        return result.scalars().all()

transaction = CRUDTransaction(Transaction)
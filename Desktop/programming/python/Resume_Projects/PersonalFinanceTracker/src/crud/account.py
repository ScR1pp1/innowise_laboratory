from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDBase
from src.models.account import Account
from src.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_multi_by_owner(self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Account]:
        result = await db.execute(
            select(Account)
            .where(
                Account.owner_id == owner_id,
                Account.is_active == True
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_owner(self, db: AsyncSession, *, obj_in: AccountCreate, owner_id: int) -> Account:
        obj_in_data = obj_in.model_dump()
        db_obj = Account(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_balance(self, db: AsyncSession, *, db_obj: Account, amount: float) -> Account:
        db_obj.balance += amount
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

account = CRUDAccount(Account)
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account
from src.models.transaction import Transaction, TransactionType


class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transaction(self, transaction_data, user_id: int) -> Transaction:
        account = await self.db.get(Account, transaction_data.account_id)
        if not account or account.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Account not found")

        if (transaction_data.type == TransactionType.EXPENSE and
                account.balance < transaction_data.amount):
            raise HTTPException(
                status_code=400,
                detail="Insufficient funds"
            )

        transaction = Transaction(**transaction_data.model_dump(), owner_id=user_id)

        if transaction_data.type == TransactionType.INCOME:
            account.balance += transaction_data.amount
        else:
            account.balance -= transaction_data.amount

        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def update_transaction(self, transaction_id: int, update_data, user_id: int) -> Transaction:
        transaction = await self.db.get(Transaction, transaction_id)
        if not transaction or transaction.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Transaction not found")

        old_amount = transaction.amount
        old_type = transaction.type
        account = await self.db.get(Account, transaction.account_id)

        if old_type == TransactionType.INCOME:
            account.balance -= old_amount
        else:
            account.balance += old_amount

        for field, value in update_data.items():
            if hasattr(transaction, field):
                setattr(transaction, field, value)

        new_amount = transaction.amount
        if (transaction.type == TransactionType.EXPENSE and
                account.balance < new_amount):
            if old_type == TransactionType.INCOME:
                account.balance += old_amount
            else:
                account.balance -= old_amount
            raise HTTPException(status_code=400, detail="Insufficient funds")

        if transaction.type == TransactionType.INCOME:
            account.balance += new_amount
        else:
            account.balance -= new_amount

        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
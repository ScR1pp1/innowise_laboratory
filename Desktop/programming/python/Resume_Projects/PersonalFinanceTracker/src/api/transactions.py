from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import get_current_active_user
from src.dependencies import get_async_db
from src.models.user import User
from src.schemas.transaction import TransactionResponse, TransactionCreate, TransactionUpdate, TransactionType

from src.crud.transaction import transaction as crud_transaction
from src.models.account import Account
from src.models.category import Category

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def read_transactions(
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        type: Optional[TransactionType] = None,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db)
):
    if any([start_date, end_date, type, category_id, account_id]):
        transactions = await crud_transaction.get_filtered_by_owner(
            db,
            owner_id=current_user.id,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            type=type.value if type else None,
            category_id=category_id,
            account_id=account_id,
        )
    else:
        transactions = await crud_transaction.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
        transaction_in: TransactionCreate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db),
):
    account = await db.get(Account, transaction_in.account_id)
    if not account or account.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account_id")

    if transaction_in.category_id is not None:
        category = await db.get(Category, transaction_in.category_id)
        if not category or category.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category_id")

    transaction = await crud_transaction.create_with_owner(db, obj_in=transaction_in, owner_id=current_user.id)
    return transaction

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def read_transaction(
        transaction_id: int,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db),
):
    transaction = await crud_transaction.get_by_owner(db, id=transaction_id, owner_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_in: TransactionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    if transaction_in.account_id is not None:
        account = await db.get(Account, transaction_in.account_id)
        if not account or account.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account_id")

    if transaction_in.category_id is not None:
        category = await db.get(Category, transaction_in.category_id)
        if not category or category.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category_id")

    transaction = await crud_transaction.update(db, id=transaction_id, owner_id=current_user.id, obj_in=transaction_in)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    transaction = await crud_transaction.soft_delete(db, id=transaction_id, owner_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

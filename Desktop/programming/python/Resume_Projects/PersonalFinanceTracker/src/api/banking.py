from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_active_user
from src.dependencies import get_async_db
from src.models import User
from src.services.open_banking_service import OpenBankingService

router = APIRouter()

@router.post("/connect-bank")
async def connect_bank_account(
    bank_name: str,
    credentials: Dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    banking_service = OpenBankingService(db)
    consent_id = await banking_service.connect_bank_account(current_user.id, bank_name, credentials)
    return {"consent_id": consent_id, "status": "connected"}

@router.post("/sync-bank/{bank_name}")
async def sync_bank_transactions(
    bank_name: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    banking_service = OpenBankingService(db)
    transactions = await banking_service.sync_bank_transactions(current_user.id, bank_name)
    return {"synced_transactions": len(transactions), "status": "success"}
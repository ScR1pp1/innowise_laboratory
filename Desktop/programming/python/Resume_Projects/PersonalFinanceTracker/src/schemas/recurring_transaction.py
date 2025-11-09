from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.schemas.transaction import TransactionType

class RecurringTransactionBase(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None
    type: TransactionType
    category_id: Optional[int] = None
    account_id: int
    frequency: str
    start_date: datetime
    end_date: Optional[datetime] = None

class RecurringTransactionCreate(RecurringTransactionBase):
    pass

class RecurringTransactionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    frequency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class RecurringTransactionResponse(RecurringTransactionBase):
    id: int
    owner_id: int
    next_occurrence: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
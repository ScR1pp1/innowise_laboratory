from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict
from pydantic import field_validator

from src.models.main import TransactionStatus
from src.schemas.tag import TagResponse


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionBase(BaseModel):
    amount: float
    type: TransactionType
    description: Optional[str] = None
    currency: str
    account_id: int
    category_id: Optional[int] = None

    @field_validator("amount")
    @classmethod
    def validate_amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("currency")
    @classmethod
    def validate_currency_code(cls, v: str) -> str:
        if len(v) != 3 or not v.isalpha():
            raise ValueError("Currency must be a 3-letter code")
        return v.upper()

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    account_id: Optional[int] = None
    category_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    amount: float
    description: str
    date: datetime
    type: str
    account_id: int
    category_id: Optional[int] = None
    owner_id: int
    currency: str
    is_recurring: bool
    recurring_interval: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True)
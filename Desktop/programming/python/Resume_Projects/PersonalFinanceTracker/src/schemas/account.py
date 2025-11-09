from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class AccountType(str, Enum):
    CASH = "cash"
    BANK_ACCOUNT = "bank_account"
    CREDIT_CARD = "credit_card"
    DIGITAL_WALLET = "digital_wallet"
    INVESTMENT = "investment"

class AccountBase(BaseModel):
    name: str
    type: AccountType
    balance: float = 0.0
    currency: str = "BYN"

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[float] = None
    currency: Optional[str] = None
    is_active: Optional[bool] = None

class AccountResponse(AccountBase):
    id: int
    owner_id: int
    initial_balance: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
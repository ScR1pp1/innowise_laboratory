from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: str
    preferred_currency: str

class UserCreate(UserBase):
    password: str
    phone_number: str
    home_address: str
    preferred_currency: str

class UserUpdate(BaseModel):
    model_config = ConfigDict()

    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    home_address: Optional[str] = None
    preferred_currency: Optional[str] = None
    timezone: Optional[str] = None
    monthly_income_goal: Optional[float] = None
    monthly_expense_limit: Optional[float] = None

class UserResponse(UserBase):
    id: int
    phone_number: str
    home_address: str
    timezone: str
    is_active: bool
    monthly_income_goal: Optional[float] = None
    monthly_expense_limit: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


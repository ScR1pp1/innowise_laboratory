from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.category import CategoryResponse
from src.schemas.tag import TagResponse


class BudgetBase(BaseModel):
    name: str
    amount: float
    period: str
    start_date: datetime
    end_date: datetime
    category_id: Optional[int] = None
    tag_id: Optional[int] = None
    currency: str = "BYN"

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    period: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category_id: Optional[int] = None
    tag_id: Optional[int] = None

class BudgetResponse(BudgetBase):
    id: int
    owner_id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    tag: Optional[TagResponse] = None
    model_config = ConfigDict(from_attributes=True)

class BudgetAnalysis(BaseModel):
    budget: BudgetResponse
    spent: float
    remaining: float
    percentage_used: float
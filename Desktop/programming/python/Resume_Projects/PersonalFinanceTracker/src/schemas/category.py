from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.models.main import TransactionType


class CategoryBase(BaseModel):
    name: str
    type: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    owner_id: int
    is_system: bool
    created_at: datetime
    children: List['CategoryResponse'] = []
    model_config = ConfigDict(from_attributes=True)
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class GoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    remaining_amount: float = 0.0
    deadline: Optional[datetime] = None
    currency: str = "BYN"

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    remaining_amount: Optional[float] = None
    deadline: Optional[datetime] = None
    currency: Optional[str] = None

class GoalResponse(GoalBase):
    id: int
    owner_id: int
    created_at: datetime
    progress_percentage: float
    remaining_amount: float
    is_completed: bool
    model_config = ConfigDict(from_attributes=True)

class GoalProgressInfo(BaseModel):
    goal_id: int
    name: str
    target_amount: float
    current_amount: float
    remaining_amount: float
    progress_percentage: float
    is_completed: bool
    currency: str
    deadline: Optional[datetime] = None
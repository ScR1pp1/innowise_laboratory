from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.crud.base import CRUDBase
from src.models.goal import Goal
from src.schemas.goal import GoalCreate, GoalUpdate


class CRUDGoal(CRUDBase[Goal, GoalCreate, GoalUpdate]):
    async def get_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Goal]:
        result = await db.execute(
            select(Goal)
            .where(Goal.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Goal.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_owner_and_id(
        self, db: AsyncSession, *, owner_id: int, goal_id: int
    ) -> Optional[Goal]:
        result = await db.execute(
            select(Goal)
            .where(Goal.id == goal_id)
            .where(Goal.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def create_for_owner(
        self, db: AsyncSession, *, obj_in: GoalCreate, owner_id: int
    ) -> Goal:
        obj_in_data = obj_in.model_dump()
        obj_in_data["owner_id"] = owner_id
        
        target_amount = obj_in_data.get("target_amount", 0)
        current_amount = obj_in_data.get("current_amount", 0)
        obj_in_data["remaining_amount"] = max(0, target_amount - current_amount)
        
        db_obj = Goal(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_progress(
        self, db: AsyncSession, *, goal_id: int, owner_id: int, amount: float
    ) -> Optional[Goal]:
        goal = await self.get_by_owner_and_id(db, owner_id=owner_id, goal_id=goal_id)
        if not goal:
            return None
        
        goal.current_amount += amount
        goal.remaining_amount = max(0, goal.target_amount - goal.current_amount)
        
        await db.commit()
        await db.refresh(goal)
        return goal

    async def update_remaining_amount(self, db: AsyncSession, goal: Goal) -> None:
        goal.remaining_amount = max(0, goal.target_amount - goal.current_amount)
        await db.commit()

    async def get_progress_info(self, goal: Goal) -> dict:
        remaining_amount = max(0, goal.target_amount - goal.current_amount)
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        
        return {
            "goal_id": goal.id,
            "name": goal.name,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "remaining_amount": remaining_amount,
            "progress_percentage": min(100, progress_percentage),
            "is_completed": goal.current_amount >= goal.target_amount,
            "currency": goal.currency,
            "deadline": goal.deadline
        }


goal = CRUDGoal(Goal)

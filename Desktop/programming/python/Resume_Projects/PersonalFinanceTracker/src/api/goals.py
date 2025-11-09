from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.dependencies import get_async_db
from src.auth import get_current_user
from src.crud.goal import goal
from src.schemas.goal import GoalCreate, GoalUpdate, GoalResponse, GoalProgressInfo
from src.models.user import User

router = APIRouter()


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    db_goal = await goal.create_for_owner(
        db=db, obj_in=goal_data, owner_id=current_user.id
    )

    progress_info = await goal.get_progress_info(db_goal)

    return GoalResponse(
        id=db_goal.id,
        name=db_goal.name,
        target_amount=db_goal.target_amount,
        current_amount=db_goal.current_amount,
        deadline=db_goal.deadline,
        currency=db_goal.currency,
        owner_id=db_goal.owner_id,
        created_at=db_goal.created_at,
        progress_percentage=progress_info["progress_percentage"],
        remaining_amount=progress_info["remaining_amount"],
        is_completed=progress_info["is_completed"]
    )


@router.get("/", response_model=List[GoalResponse])
async def get_goals(
    skip: Annotated[int, Query(description="Number of missed records")] = 0,
    limit: Annotated[int, Query(description="Maximum number of records")] = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    goals = await goal.get_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    
    result = []
    for db_goal in goals:
        progress_info = await goal.get_progress_info(db_goal)
        result.append(GoalResponse(
            id=db_goal.id,
            name=db_goal.name,
            target_amount=db_goal.target_amount,
            current_amount=db_goal.current_amount,
            deadline=db_goal.deadline,
            currency=db_goal.currency,
            owner_id=db_goal.owner_id,
            created_at=db_goal.created_at,
            progress_percentage=progress_info["progress_percentage"],
            remaining_amount=progress_info["remaining_amount"],
            is_completed=progress_info["is_completed"]
        ))
    
    return result


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    db_goal = await goal.get_by_owner_and_id(
        db=db, owner_id=current_user.id, goal_id=goal_id
    )
    
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    progress_info = await goal.get_progress_info(db_goal)
    
    return GoalResponse(
        id=db_goal.id,
        name=db_goal.name,
        target_amount=db_goal.target_amount,
        current_amount=db_goal.current_amount,
        deadline=db_goal.deadline,
        currency=db_goal.currency,
        owner_id=db_goal.owner_id,
        created_at=db_goal.created_at,
        progress_percentage=progress_info["progress_percentage"],
        remaining_amount=progress_info["remaining_amount"],
        is_completed=progress_info["is_completed"]
    )


@router.get("/{goal_id}/progress", response_model=GoalProgressInfo)
async def get_goal_progress(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    db_goal = await goal.get_by_owner_and_id(
        db=db, owner_id=current_user.id, goal_id=goal_id
    )
    
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    progress_info = await goal.get_progress_info(db_goal)
    return GoalProgressInfo(**progress_info)


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    name: Annotated[Optional[str], Query(description="New goal name")] = None,
    target_amount: Annotated[Optional[float], Query(description="New target amount")] = None,
    current_amount: Annotated[Optional[float], Query(description="New current amount")] = None,
    deadline: Annotated[Optional[datetime], Query(description="New deadline")] = None,
    currency: Annotated[Optional[str], Query(description="New currency")] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if target_amount is not None:
        update_data["target_amount"] = target_amount
    if current_amount is not None:
        update_data["current_amount"] = current_amount
    if deadline is not None:
        update_data["deadline"] = deadline
    if currency is not None:
        update_data["currency"] = currency
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be filled in"
        )
    
    db_goal = await goal.update(
        db=db,
        obj_in=update_data,
        id=goal_id,
        owner_id=current_user.id
    )
    
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    await goal.update_remaining_amount(db, db_goal)
    
    progress_info = await goal.get_progress_info(db_goal)
    
    return GoalResponse(
        id=db_goal.id,
        name=db_goal.name,
        target_amount=db_goal.target_amount,
        current_amount=db_goal.current_amount,
        deadline=db_goal.deadline,
        currency=db_goal.currency,
        owner_id=db_goal.owner_id,
        created_at=db_goal.created_at,
        progress_percentage=progress_info["progress_percentage"],
        remaining_amount=progress_info["remaining_amount"],
        is_completed=progress_info["is_completed"]
    )


@router.post("/{goal_id}/add-money", response_model=GoalProgressInfo)
async def add_money_to_goal(
    goal_id: int,
    amount: Annotated[float, Query(description="Amount to add to the progress")],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )
    
    updated_goal = await goal.update_progress(
        db=db, goal_id=goal_id, owner_id=current_user.id, amount=amount
    )
    
    if not updated_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    progress_info = await goal.get_progress_info(updated_goal)
    return GoalProgressInfo(**progress_info)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    db_goal = await goal.get_by_owner_and_id(
        db=db, owner_id=current_user.id, goal_id=goal_id
    )
    
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    await goal.remove(db=db, id=goal_id)
    return None

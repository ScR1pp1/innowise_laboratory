from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import get_current_active_user
from src.core.security import verify_password, get_password_hash
from src.dependencies import get_async_db
from src.models import User
from src.schemas.user import UserUpdate, UserResponse

from src.crud.fixeduser import update_user

router = APIRouter()


@router.put("/update_user_info", response_model=UserResponse)
async def update_user_info(
        user_in: UserUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db),
):
    update_data = user_in.model_dump(exclude_unset=True, exclude_none=True)

    if "password" in update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use /change_password endpoint for password updates"
        )

    user = await update_user(db, user_id=current_user.id, update_data=update_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/change_password")
async def change_password(
        current_password: str = Query(..., description="Current password"),
        new_password: str = Query(..., min_length=6, description="New password"),
        confirm_password: str = Query(..., min_length=6, description="Confirm password"),
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db)
):
    if new_password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password don't match")

    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    if verify_password(new_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different from the old one")

    current_user.hashed_password = get_password_hash(new_password)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Password changed successfully"}
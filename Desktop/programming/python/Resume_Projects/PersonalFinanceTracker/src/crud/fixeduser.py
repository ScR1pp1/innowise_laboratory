from fastapi import HTTPException
from sqlalchemy import select
from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models import User


async def update_user(
        db: AsyncSession,
        *,
        user_id: int,
        update_data: Dict[str, Any]
) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return None

    print(f"🔍 DEBUG Before update - User: {user.id}, Data: {update_data}")

    for field, value in update_data.items():
        if hasattr(user, field) and value is not None:
            print(f"🔍 Setting {field} to {value} (type: {type(value)})")
            setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user
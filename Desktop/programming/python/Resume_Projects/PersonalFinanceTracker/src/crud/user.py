from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.crud.base import CRUDBase
from src.core.security import verify_password, get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        if len(obj_in.password.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            phone_number = obj_in.phone_number,
            home_address=obj_in.home_address,
            hashed_password=hashed_password,
            preferred_currency=getattr(obj_in, 'preferred_currency', 'BYN'),
            timezone=getattr(obj_in, 'timezone', 'UTC')
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

user = CRUDUser(User)
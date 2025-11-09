from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.security import create_access_token, verify_password, get_password_hash
from src.auth import get_current_active_user, get_current_user
from src.config import settings
from src.dependencies import get_async_db
from src.models.user import User
from src.schemas.token import Token
from src.schemas.user import UserResponse, UserCreate

from src.crud.user import user as crud_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_async_db)
):
    existing_user = await crud_user.get_by_username(db, username = user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already in use"
        )
    existing_email = await crud_user.get_by_email(db, email=user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    user = await crud_user.create(db, obj_in=user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_db),
):
    user = await crud_user.authenticate(db, username = form_data.username, password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.username})

    return Token(
        access_token = access_token,
        token_type = "bearer",
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        username = user.username,
        user_id = user.id,
        preferred_currency = user.preferred_currency
    )

@router.get("/me", response_model = UserResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
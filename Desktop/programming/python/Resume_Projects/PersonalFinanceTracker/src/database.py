from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()
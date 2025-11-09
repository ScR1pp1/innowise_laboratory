import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, created_at, updated_at


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(unique=True, index=True)
    home_address: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    preferred_currency: Mapped[str] = mapped_column(default="BYN")
    timezone: Mapped[str] = mapped_column(default="UTC")
    is_active: Mapped[bool] = mapped_column(default=True)
    monthly_income_goal: Mapped[Optional[float]]
    monthly_expense_limit: Mapped[Optional[float]]

    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    categories = relationship("Category", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    tags = relationship("Tag", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    budgets = relationship("Budget", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    goals = relationship("Goal", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    recurring_transactions = relationship("RecurringTransaction", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(unique=True, index=True)
    expired_at: Mapped[datetime.datetime]
    created_at: Mapped[created_at]

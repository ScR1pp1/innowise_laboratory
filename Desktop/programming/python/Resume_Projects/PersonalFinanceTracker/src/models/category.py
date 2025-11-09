from typing import Optional

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, TransactionType, created_at


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(index=True)
    id: Mapped[intpk]
    type: Mapped[Optional[TransactionType]] = mapped_column(Enum(TransactionType))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    icon: Mapped[Optional[str]]
    color: Mapped[Optional[str]]
    is_system: Mapped[bool] = mapped_column(default=False)  # нельзя удалять
    created_at: Mapped[created_at]

    owner = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    budgets = relationship("Budget", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    recurring_transactions = relationship("RecurringTransaction", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    # parent = relationship("Category", back_populates="children", remote_side=[id])
    # children = relationship("Category", back_populates="parent", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

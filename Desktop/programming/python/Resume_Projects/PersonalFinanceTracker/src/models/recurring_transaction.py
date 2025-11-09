import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, created_at, updated_at
from src.models.main import TransactionType


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id: Mapped[intpk]
    name: Mapped[str]
    amount: Mapped[float]
    description: Mapped[Optional[str]]
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    frequency: Mapped[str]
    next_occurrence: Mapped[Optional[datetime.datetime]]
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[Optional[datetime.datetime]]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(default=True)

    owner = relationship("User", back_populates="recurring_transactions")
    category = relationship("Category", back_populates="recurring_transactions")
    account = relationship("Account", back_populates="recurring_transactions")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
import datetime
from typing import Optional, List

from sqlalchemy import Enum, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, TransactionType, created_at, updated_at, transaction_tags, TransactionStatus


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[intpk]
    amount: Mapped[float] = mapped_column(index=True)
    description: Mapped[Optional[str]]
    date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), index=True)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    currency: Mapped[str] = mapped_column(default="BYN")
    is_recurring: Mapped[bool] = mapped_column(default=False)
    recurring_interval: Mapped[Optional[str]]
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.COMPLETED)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    owner = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    tags = relationship("Tag", secondary=transaction_tags, back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, amount='{self.amount}', type='{self.type.value}')>"


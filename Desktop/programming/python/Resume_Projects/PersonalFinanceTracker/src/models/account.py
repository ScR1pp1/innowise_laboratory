import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, created_at, updated_at


class AccountType(enum.Enum):
    CASH = "cash"
    BANK_ACCOUNT = "bank_account"
    CREDIT_CARD = "credit_card"
    DIGITAL_WALLET = "digital_wallet"
    INVESTMENT = "investment"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[AccountType]
    balance: Mapped[float] = mapped_column(default=0.0)
    initial_balance: Mapped[float] = mapped_column(default=0.0)
    currency: Mapped[str] = mapped_column(default="BYN")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(default=True)

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan", passive_deletes=True)
    recurring_transactions = relationship("RecurringTransaction", back_populates="account", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

    @property
    def current_balance(self):
        return self.balance
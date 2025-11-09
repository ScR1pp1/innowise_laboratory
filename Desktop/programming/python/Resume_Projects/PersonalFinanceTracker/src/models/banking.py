from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.main import intpk, created_at


class BankConnection(Base):
    __tablename__ = "bank_connections"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    bank_name: Mapped[str]
    consent_id: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    connected_at: Mapped[created_at]
    last_sync_at: Mapped[Optional[datetime.datetime]]
    sync_status: Mapped[str] = mapped_column(default="pending")

    encrypted_credentials: Mapped[Optional[str]]


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[intpk]
    connection_id: Mapped[int] = mapped_column(ForeignKey("bank_connections.id", ondelete="CASCADE"))
    bank_account_id: Mapped[str]
    account_number: Mapped[str]
    balance: Mapped[float]
    currency: Mapped[str]
    account_type: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
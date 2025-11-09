import datetime
from typing import Optional, Annotated

from sqlalchemy import Column, Integer, String, Float, MetaData, ForeignKey, Enum, text, func, Table, MappingResult
from sqlalchemy.orm import mapped_column
import enum

from src.database import Base

intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


transaction_tags = Table(
    "transaction_tags",
    Base.metadata,
    Column("transaction_id", Integer, ForeignKey("transactions.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CurrencyChoose(str, enum.Enum):
    BYN = "BYN"
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"
    AED = "AED"
    CZK = "CZK"
    






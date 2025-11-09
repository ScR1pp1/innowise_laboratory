from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, transaction_tags


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(index=True)
    color: Mapped[Optional[str]]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="tags")
    transactions = relationship("Transaction", secondary=transaction_tags, back_populates="tags", passive_deletes=True)
    budgets = relationship("Budget", back_populates="tag", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
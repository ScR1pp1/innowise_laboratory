import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[intpk]
    name: Mapped[str]
    amount: Mapped[float]
    period: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    currency: Mapped[str] = mapped_column(default="BYN")

    owner = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
    tag = relationship("Tag", back_populates="budgets")

    __table_args__ = (
        Index('ix_budgets_owner_period', 'owner_id', 'period'),
        Index('ix_budgets_dates', 'start_date', 'end_date'),
        CheckConstraint('end_date > start_date', name='check_dates_valid'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.category_id and not self.tag_id:
            raise ValueError("Budget must have either category_id or tag_id")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
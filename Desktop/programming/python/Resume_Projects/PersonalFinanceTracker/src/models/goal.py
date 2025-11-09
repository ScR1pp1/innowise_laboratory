import datetime
from typing import Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[intpk]
    name: Mapped[str]
    target_amount: Mapped[float]
    current_amount: Mapped[float] = mapped_column(default=0.0)
    remaining_amount: Mapped[float] = mapped_column(default=0.0)
    deadline: Mapped[Optional[datetime.datetime]]
    currency: Mapped[str] = mapped_column(default="BYN")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    owner = relationship("User", back_populates="goals")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
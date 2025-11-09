import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.main import intpk, CurrencyChoose


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[intpk]
    code: Mapped[CurrencyChoose] = mapped_column(unique=True, index=True)  # USD, EUR, BYN
    name: Mapped[str]
    symbol: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[intpk]
    from_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))
    to_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))
    rate: Mapped[float]
    date: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    from_currency = relationship("Currency", foreign_keys=[from_currency_id])
    to_currency = relationship("Currency", foreign_keys=[to_currency_id])

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
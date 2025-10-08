import datetime

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.types import DateTime, Text

from core.models import Base
from core.models.users import User


class TokenSubscription(Base):
    __tablename__ = 'token_subscriptions'

    id = Column(Integer, primary_key=True, unique=True)
    telegram_id = Column(
        Integer,
        ForeignKey(User.telegram_id),
        index=True
    )
    symbol = Column(Text, default=None)
    sign = Column(Text, default=None)
    price = Column(Float, default=0)
    market_type = Column(Text, default=None)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    muted_1h_at = Column(
        DateTime(timezone=True),
        default=None
    )
    muted_24h_at = Column(
        DateTime(timezone=True),
        default=None
    )

    def __str__(self) -> str:
        return f"{self.id}"

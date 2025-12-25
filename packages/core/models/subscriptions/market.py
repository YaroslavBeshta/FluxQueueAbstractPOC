import datetime

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.types import DateTime, Text

from core.models import Base, User


class MarketSubscription(Base):
    __tablename__ = "market_subscriptions"

    id = Column(Integer, primary_key=True, unique=True)
    telegram_id = Column(Integer, ForeignKey(User.telegram_id), index=True)
    sign = Column(Text, default=None)
    percent = Column(Integer, default=50)
    market_type = Column(Text, default=None)
    created_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
    muted_1h_at = Column(DateTime(timezone=True), default=None)
    muted_24h_at = Column(DateTime(timezone=True), default=None)

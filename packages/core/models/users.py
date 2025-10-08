import datetime

from sqlalchemy import Column, Integer
from sqlalchemy.types import Boolean, DateTime, Text

from core.models.base import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(Text, default=None)
    last_name = Column(Text, default=None)
    username = Column(Text, default=None)
    language_code = Column(Text)
    is_bot = Column(Boolean)
    is_premium = Column(Boolean)
    disabled = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now()
    )

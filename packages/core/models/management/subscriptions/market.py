import datetime

from sqlalchemy import or_

from core import session_scope
from core.common.utils import send_telegram_log
from core.models import MarketSubscription


def get_market_subscriptions(
    telegram_id: int = None, market_type: str = None, include_muted: bool = False
) -> list:
    with session_scope() as session:
        query = session.query(MarketSubscription)
        if telegram_id:
            query = query.filter(MarketSubscription.telegram_id == telegram_id)
        if market_type:
            query = query.filter(MarketSubscription.market_type == market_type)
        if not include_muted:
            query = query.filter(
                MarketSubscription.muted_1h_at == None,
                MarketSubscription.muted_24h_at == None,
            )
        subscriptions = query.all()
        # Access all attributes while session is active to ensure they're loaded
        # Then expunge to detach objects from session so they can be used outside
        for sub in subscriptions:
            # Touch all attributes that will be accessed later
            _ = (sub.telegram_id, sub.market_type, sub.sign, sub.percent,
                 sub.muted_1h_at, sub.muted_24h_at)
            session.expunge(sub)
        return subscriptions


def upsert_market_subscription(
    telegram_id: int, market_type: str, sign: str, percent: int
) -> None:
    with session_scope() as session:
        query = session.query(MarketSubscription)
        query = query.filter(
            MarketSubscription.telegram_id == telegram_id,
            MarketSubscription.market_type == market_type,
            MarketSubscription.sign == sign,
        )
        subscription = query.first()

        if subscription:
            subscription.percent = percent
            subscription.sign = sign
        else:
            subscription = MarketSubscription(
                telegram_id=telegram_id, market_type=market_type, sign=sign, percent=percent
            )

        try:
            session.add(subscription)
            # commit happens automatically in session_scope
        except Exception as e:
            send_telegram_log(e)
            raise  # Re-raise to trigger rollback in session_scope


def delete_market_subscription(
    telegram_id: int, market_type: str = None, *args
) -> None:
    with session_scope() as session:
        query = session.query(MarketSubscription)
        query = query.filter(MarketSubscription.telegram_id == telegram_id)

        if market_type:
            query = query.filter(MarketSubscription.market_type == market_type)

        try:
            query.delete()
            # commit happens automatically in session_scope
        except Exception as e:
            send_telegram_log(e)
            raise  # Re-raise to trigger rollback in session_scope


def unmute_market_subscriptions():
    with session_scope() as session:
        # Calculate thresholds once, not in the loop
        now = datetime.datetime.now(datetime.timezone.utc)
        threshold_1h = now - datetime.timedelta(hours=1)
        threshold_24h = now - datetime.timedelta(hours=24)
        
        query = session.query(MarketSubscription)
        query = query.filter(
            or_(
                MarketSubscription.muted_1h_at != None,
                MarketSubscription.muted_24h_at != None,
            )
        )

        subscriptions = query.all()
        for subscription in subscriptions:
            if subscription.muted_1h_at and threshold_1h > subscription.muted_1h_at:
                subscription.muted_1h_at = None
            if subscription.muted_24h_at and threshold_24h > subscription.muted_24h_at:
                subscription.muted_24h_at = None
            # All changes are tracked automatically, commit happens at end of context
        # Single commit for all changes - much more efficient


def unmute_market_subscription(telegram_id: int, market_type: str, *args) -> None:
    with session_scope() as session:
        query = session.query(MarketSubscription)
        query = query.filter(
            MarketSubscription.telegram_id == telegram_id,
            MarketSubscription.market_type == market_type,
        )

        subscription = query.first()
        if subscription:
            subscription.muted_1h_at = None
            subscription.muted_24h_at = None
            try:
                session.add(subscription)
                # commit happens automatically in session_scope
            except Exception as e:
                send_telegram_log(e)
                raise  # Re-raise to trigger rollback in session_scope


def mute_market_subscription(telegram_id: int, market_type: str, mute_time: str, *args):
    with session_scope() as session:
        query = session.query(MarketSubscription)
        query = query.filter(
            MarketSubscription.telegram_id == telegram_id,
            MarketSubscription.market_type == market_type,
        )

        subscription = query.first()
        if subscription:
            if mute_time == "1h":
                subscription.muted_1h_at = datetime.datetime.now(datetime.timezone.utc)
            if mute_time == "24h":
                subscription.muted_24h_at = datetime.datetime.now(datetime.timezone.utc)

            try:
                session.add(subscription)
                # commit happens automatically in session_scope
            except Exception as e:
                send_telegram_log(e)
                raise  # Re-raise to trigger rollback in session_scope

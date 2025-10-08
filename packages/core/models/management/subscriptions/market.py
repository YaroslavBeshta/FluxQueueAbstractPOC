import datetime

from sqlalchemy import or_

from core import session
from core.common.utils import send_telegram_log
from core.models import MarketSubscription


def get_market_subscriptions(telegram_id: int = None, market_type: str = None, include_muted: bool = False) -> list:
    query = session.query(MarketSubscription)
    if telegram_id:
        query = query.filter(MarketSubscription.telegram_id == telegram_id)
    if market_type:
        query = query.filter(MarketSubscription.market_type == market_type)
    if not include_muted:
        query = query.filter(
            MarketSubscription.muted_1h_at == None,
            MarketSubscription.muted_24h_at == None
        )
    subscriptions = query.all()
    return subscriptions


def upsert_market_subscription(telegram_id: int, market_type: str, percent: int) -> None:
    query = session.query(MarketSubscription)
    query = query.filter(
        MarketSubscription.telegram_id == telegram_id,
        MarketSubscription.market_type == market_type,
    )
    subscription = query.first()

    if subscription:
        subscription.percent = percent
    else:
        subscription = MarketSubscription(
            telegram_id=telegram_id,
            market_type=market_type,
            percent=percent
        )

    try:
        session.add(subscription)
        session.commit()
    except Exception as e:
        send_telegram_log(e)
    finally:
        session.close()


def delete_market_subscription(telegram_id: int, market_type: str = None, *args) -> None:
    query = session.query(MarketSubscription)
    query = query.filter(MarketSubscription.telegram_id == telegram_id)

    if market_type:
        query = query.filter(MarketSubscription.market_type == market_type)

    try:
        query.delete()
        session.commit()
    except Exception as e:
        send_telegram_log(e)
    finally:
        session.close()


def unmute_market_subscriptions():
    query = session.query(MarketSubscription)
    query = query.filter(
        or_(
            MarketSubscription.muted_1h_at != None,
            MarketSubscription.muted_24h_at != None
        )
    )

    subscriptions = query.all()
    for subscription in subscriptions:
        if subscription.muted_1h_at:
            now = datetime.datetime.now(
                datetime.timezone.utc
            ) - datetime.timedelta(hours=1)
            if now > subscription.muted_1h_at:
                subscription.muted_1h_at = None
        if subscription.muted_24h_at:
            now = datetime.datetime.now(
                datetime.timezone.utc
            ) - datetime.timedelta(hours=24)
            if now > subscription.muted_24h_at:
                subscription.muted_24h_at = None
        try:
            session.add(subscription)
            session.commit()
        except Exception as e:
            send_telegram_log(e)


def unmute_market_subscription(telegram_id: int, market_type: str, *args) -> None:
    query = session.query(MarketSubscription)
    query = query.filter(
        MarketSubscription.telegram_id == telegram_id,
        MarketSubscription.market_type == market_type
    )

    subscription = query.first()
    if subscription:
        subscription.muted_1h_at = None
        subscription.muted_24h_at = None
        try:
            session.add(subscription)
            session.commit()
        except Exception as e:
            send_telegram_log(e)
        finally:
            session.close()


def mute_market_subscription(telegram_id: int, market_type: str, mute_time: str, *args):
    query = session.query(MarketSubscription)
    query = query.filter(
        MarketSubscription.telegram_id == telegram_id,
        MarketSubscription.market_type == market_type
    )

    subscription = query.first()
    if subscription:
        if mute_time == "1h":
            subscription.muted_1h_at = datetime.datetime.now(
                datetime.timezone.utc)
        if mute_time == "24h":
            subscription.muted_24h_at = datetime.datetime.now(
                datetime.timezone.utc)

        try:
            session.add(subscription)
            session.commit()
        except Exception as e:
            send_telegram_log(e)
        finally:
            session.close()

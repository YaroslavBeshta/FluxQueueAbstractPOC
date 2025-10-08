import datetime

from sqlalchemy import or_

from core import session
from core.common.utils import send_telegram_log
from core.models import TokenSubscription


def get_token_subscriptions(telegram_id: int = None, market_type: str = None, include_muted: bool = False) -> list:
    query = session.query(TokenSubscription)
    if telegram_id:
        query = query.filter(TokenSubscription.telegram_id == telegram_id)
    if market_type:
        query = query.filter(TokenSubscription.market_type == market_type)
    if not include_muted:
        query = query.filter(
            TokenSubscription.muted_1h_at == None,
            TokenSubscription.muted_24h_at == None
        )
    subscriptions = query.all()
    return subscriptions


def get_tokens_by_market_type(market_type: str) -> list:
    query = session.query(TokenSubscription.symbol)
    query = query.filter(TokenSubscription.market_type == market_type)
    subscriptions = query.all()
    return subscriptions


def upsert_token_subscription(telegram_id: int, symbol: str, sign: str, market_type: str, price: float) -> None:
    query = session.query(TokenSubscription)
    query = query.filter(
        TokenSubscription.telegram_id == telegram_id,
        TokenSubscription.symbol == symbol,
        TokenSubscription.sign == sign,
        TokenSubscription.market_type == market_type,
    )
    subscription = query.first()

    if subscription:
        subscription.price = price
        subscription.muted_1h_at = None
        subscription.muted_24h_at = None
    else:
        subscription = TokenSubscription(
            telegram_id=telegram_id,
            symbol=symbol,
            sign=sign,
            market_type=market_type,
            price=price
        )

    try:
        session.add(subscription)
        session.commit()
    except Exception as e:
        send_telegram_log(e)
    finally:
        session.close()


def delete_token_subscription(telegram_id: int, symbol: str = None, market_type: str = None, *args) -> None:
    query = session.query(TokenSubscription)
    query = query.filter(
        TokenSubscription.telegram_id == telegram_id
    )

    if symbol and symbol != "all":
        symbol = symbol.upper()
        query = query.filter(TokenSubscription.symbol == symbol)
    if market_type:
        query = query.filter(TokenSubscription.market_type == market_type)

    try:
        query.delete()
        session.commit()
    except Exception as e:
        send_telegram_log(e)
    finally:
        session.close()


def unmute_token_subscriptions():
    query = session.query(TokenSubscription)
    query = query.filter(
        or_(
            TokenSubscription.muted_1h_at != None,
            TokenSubscription.muted_24h_at != None
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


def unmute_token_subscription(telegram_id: int, symbol: str, market_type: str, *args):
    query = session.query(TokenSubscription)
    query = query.filter(
        TokenSubscription.telegram_id == telegram_id,
        TokenSubscription.symbol == symbol,
        TokenSubscription.market_type == market_type
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


def mute_token_subscription(telegram_id: int, symbol: str, market_type: str, mute_time: str, *args):
    query = session.query(TokenSubscription)
    query = query.filter(
        TokenSubscription.telegram_id == telegram_id,
        TokenSubscription.symbol == symbol,
        TokenSubscription.market_type == market_type
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

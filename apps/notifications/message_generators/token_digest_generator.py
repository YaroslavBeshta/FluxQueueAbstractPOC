from core.common.mappings import INEQUALITY_OPERATOR_MAPPING
from core.common.utils import dict_upsert
from core.models.management.subscriptions.token import \
    get_token_subscriptions


def generate_message(symbol, token_price, market_type):
    if market_type == "perp":
        market_type = "FUTURES"
    market_type = market_type.upper()
    return f"🔔 {symbol} price: {token_price} <b>[{market_type}]</b>"


def generate_token_digest_messages(market_type, processed_data):
    subscriptions = get_token_subscriptions(market_type=market_type)

    notifications = {}
    for subscription in subscriptions:
        token_price = float(processed_data[subscription.symbol]["last_price"])
        if INEQUALITY_OPERATOR_MAPPING[subscription.sign](
            token_price, subscription.price
        ):
            dict_upsert(
                notifications,
                str(subscription.telegram_id),
                generate_message(subscription.symbol, token_price, market_type)
            )
    return notifications

from core.common.mappings import BINANCE_UI_URL_MAPPING
from core.common.utils import dict_upsert
from core.models.management.subscriptions.market import get_market_subscriptions

BLOCKLIST = ("SRMUSDT",)


def generate_message(symbol, pcp, market_type):
    url = BINANCE_UI_URL_MAPPING[market_type]
    return f'🚀 <a href="{url}/{symbol}">{symbol}</a>: +{pcp}%'


def generate_market_digest_messages(market_type: str, processed_data: dict) -> dict:
    subs = get_market_subscriptions(market_type=market_type)

    price_percents = {}
    for sub in subs:
        if sub.percent in price_percents:
            price_percents[sub.percent].append(str(sub.telegram_id))
        else:
            price_percents[sub.percent] = [str(sub.telegram_id)]

    notifications = {}
    for symbol, row in processed_data.items():
        if symbol[-4:] != "USDT" or symbol in BLOCKLIST:
            continue

        pcp = round(float(row["price_change_percent"]))
        for pp in price_percents:
            if pcp > pp:
                for chat_id in price_percents[pp]:
                    dict_upsert(
                        notifications,
                        chat_id,
                        generate_message(symbol, pcp, market_type),
                    )
    return notifications

from core.common.mappings import (
    BINANCE_UI_URL_MAPPING,
    INEQUALITY_OPERATOR_MAPPING,
    INEQUALITY_SIGN_MAPPING,
)
from core.common.utils import dict_upsert
from core.models.management.subscriptions.market import get_market_subscriptions

BLOCKLIST = ("SRMUSDT",)


def generate_message(symbol, pcp, market_type):
    url = BINANCE_UI_URL_MAPPING[market_type]
    add_plus = "+" if pcp > 0 else ""
    return f'🚀 <a href="{url}/{symbol}">{symbol}</a>: {add_plus}{pcp}%'


def generate_market_digest_messages(market_type: str, processed_data: dict) -> dict:
    subs = get_market_subscriptions(market_type=market_type)

    price_percents = {}
    for sub in subs:
        if sub.percent in price_percents:
            price_percents[(sub.percent, sub.sign)].append(str(sub.telegram_id))
        else:
            price_percents[(sub.percent, sub.sign)] = [str(sub.telegram_id)]

    notifications = {}
    for symbol, row in processed_data.items():
        if symbol[-4:] != "USDT" or symbol in BLOCKLIST:
            continue

        pcp = round(float(row["price_change_percent"]))
        for pp, sign in price_percents:
            if INEQUALITY_OPERATOR_MAPPING[sign](pcp, pp):
                for chat_id in price_percents[(pp, sign)]:
                    dict_upsert(
                        notifications,
                        chat_id,
                        {
                            "sign": sign,
                            "pcp": pcp,
                            "symbol": symbol,
                            "market_type": market_type,
                        },
                    )

    notifications = {
        chat_id: [
            generate_message(d["symbol"], d["pcp"], d["market_type"])
            for d in sorted(data, key=lambda x: x["pcp"], reverse=True)
        ]
        for chat_id, data in notifications.items()
    }
    return notifications

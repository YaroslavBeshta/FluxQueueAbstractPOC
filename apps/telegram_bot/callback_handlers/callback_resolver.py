from core.models.management.subscriptions.market import (
    delete_market_subscription, mute_market_subscription,
    unmute_market_subscription)
from core.models.management.subscriptions.token import (
    delete_token_subscription, mute_token_subscription,
    unmute_token_subscription)

func_mapping = {
    "market": {
        "mute": (mute_market_subscription, "🔇 {} market muted"),
        "unmute": (unmute_market_subscription, "🔈 {} market unmuted"),
        "unsub": (delete_market_subscription, "♻️ {} market unsubscribed")
    },
    "token": {
        "mute": (mute_token_subscription, "🔇 {} ({}) muted"),
        "unmute": (unmute_token_subscription, "🔈 {} ({}) unmuted"),
        "unsub": (delete_token_subscription, "♻️ {} ({}) unsubscribed")
    }
}


def resolve_callback(callback, bot):
    telegram_id = callback.from_user.id
    callback_data = callback.data.split("_")
    command, subscription_type, market_type, timing = callback_data

    f, resp_text = func_mapping[subscription_type][command]
    if subscription_type == "token":
        symbol = callback.message.text.split(" ")[1]
        f(telegram_id, symbol, market_type, timing)
        bot.answer_callback_query(callback.id, resp_text.format(symbol, market_type.title()))
    if subscription_type == "market":
        f(telegram_id, market_type, timing)
        bot.answer_callback_query(callback.id, resp_text.format(market_type.title()))

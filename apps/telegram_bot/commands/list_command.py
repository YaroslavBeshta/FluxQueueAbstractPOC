from core.models.management.subscriptions.market import get_market_subscriptions
from core.models.management.subscriptions.token import get_token_subscriptions
import messages
from utils import (
    build_market_subscriptions_message,
    build_token_subscriptions_message,
    divide_spot_and_perp,
)


def list_command(message, bot):
    telegram_id = message.from_user.id
    token_subscriptions = get_token_subscriptions(
        telegram_id=telegram_id, include_muted=True
    )
    spot_token, perp_token, stock_token = divide_spot_and_perp(token_subscriptions)

    market_subscriptions = get_market_subscriptions(
        telegram_id=telegram_id, include_muted=True
    )
    spot_market, perp_market, stock_market = divide_spot_and_perp(market_subscriptions)

    subscriptions = []
    if spot_token:
        subscriptions.append(build_token_subscriptions_message(spot_token, "spot"))
    if spot_market:
        subscriptions.append(build_market_subscriptions_message(spot_market, "spot"))
    if perp_token:
        subscriptions.append(build_token_subscriptions_message(perp_token, "futures"))
    if perp_market:
        subscriptions.append(build_market_subscriptions_message(perp_market, "futures"))
    if stock_token:
        subscriptions.append(build_token_subscriptions_message(stock_token, "stock"))

    bot.send_message(
        message.chat.id,
        messages.message_with_args(
            messages.LIST_COMMAND_SUCCESS, "".join(subscriptions)
        ),
        parse_mode="HTML",
    )

from core.models.management.subscriptions.market import \
    delete_market_subscription
from messages import DELETE_MARKET_COMMAND_SUCCESS


def delete_market_command(message, bot):
    delete_market_subscription(message.from_user.id)
    bot.send_message(
        message.chat.id,
        DELETE_MARKET_COMMAND_SUCCESS,
        parse_mode='HTML'
    )

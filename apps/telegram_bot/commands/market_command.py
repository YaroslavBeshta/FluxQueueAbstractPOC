from core.models.management.subscriptions.market import \
    upsert_market_subscription
import messages
from validation import market_command_input_validator


def market_command(message, bot):
    error_message, *input_data = market_command_input_validator(message.text)
    if not error_message:
        input_data = input_data.pop()
        upsert_market_subscription(message.chat.id, input_data[1], input_data[2], input_data[0])
        bot.send_message(
            message.chat.id,
            messages.MARKET_COMMAND_SUCCESS,
            parse_mode='HTML'
        )
    else:
        bot.send_message(
            message.chat.id,
            error_message,
            parse_mode='HTML'
        )

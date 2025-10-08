from core.models.management.subscriptions.token import \
    delete_token_subscription
import messages
from validation import delete_token_command_input_validator


def delete_token_command(message, bot):
    error_message, *input_data = delete_token_command_input_validator(message.text)
    if not error_message:
        delete_token_subscription(message.chat.id, input_data[0])
        bot.send_message(
            message.chat.id,
            messages.DELETE_COMMAND_SUCCESS,
            parse_mode='HTML'
        )
    else:
        bot.send_message(
            message.chat.id,
            messages.DELETE_COMMAND_HELP,
            parse_mode='HTML'
        )

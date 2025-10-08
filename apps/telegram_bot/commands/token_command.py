from core.common.mappings import INEQUALITY_SIGN_MAPPING
from core.models.management.subscriptions.token import \
    upsert_token_subscription
import messages
from validation import token_command_input_validator


def token_command(message, bot):
    error_message, *input_data = token_command_input_validator(message.text)
    if not error_message:
        input_data = input_data.pop()
        upsert_token_subscription(
            message.chat.id, input_data[0], input_data[2], input_data[1], input_data[3])
        bot.send_message(
            message.chat.id,
            messages.message_with_args(
                messages.TOKEN_COMMAND_SUCCESS,
                input_data[0],
                INEQUALITY_SIGN_MAPPING[input_data[2]],
                input_data[3]
            ),
            parse_mode='HTML'
        )
    else:
        bot.send_message(
            message.chat.id,
            error_message,
            parse_mode='HTML'
        )

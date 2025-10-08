from core.models.management.users import get_or_create_user_from_message
from messages import START_COMMAND_SUCCESS


def start_command(message, bot):
    get_or_create_user_from_message(message)
    bot.send_message(
        message.chat.id,
        START_COMMAND_SUCCESS,
        parse_mode='HTML'
    )

from messages import HELP_COMMAND_SUCCESS


def help_command(message, bot):
    bot.send_message(
        message.chat.id,
        HELP_COMMAND_SUCCESS,
        parse_mode='HTML'
    )

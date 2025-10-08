import os

import telebot
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, ReadTimeout

from core.common.utils import send_telegram_log
import commands
from callback_handlers import resolve_callback


def main():
    load_dotenv()
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    bot = telebot.TeleBot(API_TOKEN)

    bot.register_message_handler(
        commands.start_command, commands=["start"], pass_bot=True
    )
    bot.register_message_handler(
        commands.help_command, commands=["help"], pass_bot=True
    )
    bot.register_message_handler(
        commands.token_command, commands=["token", "tokenf"], pass_bot=True
    )
    bot.register_message_handler(
        commands.list_command, commands=["list"], pass_bot=True
    )
    bot.register_message_handler(
        commands.delete_token_command, commands=["delete"], pass_bot=True
    )
    bot.register_message_handler(
        commands.market_command, commands=["market", "marketf"], pass_bot=True
    )
    bot.register_message_handler(
        commands.delete_market_command, commands=["unsubscribe"], pass_bot=True
    )
    bot.register_callback_query_handler(resolve_callback, func=None, pass_bot=True)

    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == "__main__":
    main()

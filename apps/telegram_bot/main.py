import os
import time

from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from core.unit import load_environment_variables
from core.common.logger import setup_logging, get_logger
import telebot
import commands
from callback_handlers import resolve_callback

# Set up logging
setup_logging(service_name="telegram_bot")
logger = get_logger(__name__)


def main():
    load_environment_variables()
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not API_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

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

    # Retry loop with exponential backoff for network errors
    retry_delay = 1  # Start with 1 second
    
    while True:
        try:
            logger.info("Starting Telegram bot polling...")
            # Increased timeouts to handle slow connections better
            # timeout: how long to wait for a response (increased from 10 to 20)
            # long_polling_timeout: how long to keep connection open (increased from 5 to 10)
            bot.infinity_polling(timeout=20, long_polling_timeout=10, interval=0)
        except (ReadTimeout, ConnectionError, RequestException) as e:
            logger.warning(f"Network error (timeout/connection): {e}")
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            # Exponential backoff, but cap at 60 seconds
            retry_delay = min(retry_delay * 2, 60)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in bot polling: {e}", exc_info=True)
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
        else:
            # If we exit normally (shouldn't happen with infinity_polling), reset delay
            retry_delay = 1


if __name__ == "__main__":
    main()

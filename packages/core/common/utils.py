import os

import requests
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_CHAT_ID = os.getenv("DEFUALT_CHAT_ID")


def dict_upsert(d, key, value):
    if key not in d:
        d[key] = [value]
    else:
        d[key].append(value)
    return d


def prettify_float(number, precision=2):
    sign = ""
    if number > 0:
        sign = "+"
    number = format(number, f".{precision}f")
    return f"{sign}{number}"


def send_telegram_log(message, chat_id=DEFAULT_CHAT_ID, reply_markup=None):
    telegram_bot_token = TELEGRAM_BOT_TOKEN
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        "disable_web_page_preview": True,

    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    return requests.post(url, json=payload).content

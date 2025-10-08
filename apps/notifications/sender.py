import os

import requests
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram(chat_id, message, reply_markup=None):
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


def notify(notifications: dict, reply_markup=None) -> None:
    for chat_id, messages in notifications.items():
        for message in messages:
            send_telegram(chat_id, message, reply_markup)

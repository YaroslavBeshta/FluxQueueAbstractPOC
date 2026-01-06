import requests


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


def send_telegram_log(
    message, chat_id=None, telegram_bot_token=None, reply_markup=None
):
    if chat_id is None or telegram_bot_token is None:
        return
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    return requests.post(url, json=payload).content

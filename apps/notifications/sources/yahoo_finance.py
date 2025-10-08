import requests

from core.common.constants import USER_AGENT_MOZZILA, YAHOO_FINANCE_URL
from processors import process_yahoo_response


def fetch_yahoo_symbol(symbol: str) -> str:
    url = f"{YAHOO_FINANCE_URL}/{symbol}"
    response = requests.get(url, headers=USER_AGENT_MOZZILA)
    return response


def fetch_yahoo_symbols(symbols: list) -> dict:
    data = {}
    for symbol in symbols:
        response = fetch_yahoo_symbol(symbol)
        market_price = process_yahoo_response(response)
        data[symbol] = {"last_price": market_price}
    return data

import requests

from core.common.constants import BINANCE_PERP_TICKER_URL, BINANCE_SPOT_TICKER_URL
from core.common.utils import send_telegram_log
from utils import format_request_parameters


def fetch_binance_spot_ticker_endpoint_data(symbols=None):
    base_url = BINANCE_SPOT_TICKER_URL
    if symbols:
        base_url += format_request_parameters(symbols)
    try:
        response = requests.get(base_url)
    except Exception as e:
        send_telegram_log(f"Error connecting to binance: {e}")
        return {}
    return response.json()


def fetch_binance_perp_ticker_endpoint_data(symbols=None):
    base_url = BINANCE_PERP_TICKER_URL
    if symbols:
        base_url += format_request_parameters(symbols)
    try:
        response = requests.get(base_url)
    except Exception as e:
        send_telegram_log(f"Error connecting to binance: {e}")
        return {}
    return response.json()

import requests

from core.common.constants import BINANCE_PERP_TICKER_URL, BINANCE_SPOT_TICKER_URL
from core.common.logger import get_logger
from core.common.utils import send_telegram_log
from utils import format_request_parameters

logger = get_logger(__name__)


def fetch_binance_spot_ticker_endpoint_data(symbols=None):
    base_url = BINANCE_SPOT_TICKER_URL
    if symbols:
        base_url += format_request_parameters(symbols)
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Binance spot ticker data: {e}")
        send_telegram_log(f"Error connecting to binance spot: {e}")
        return []
    except ValueError as e:
        logger.error(f"Error parsing JSON response from Binance spot: {e}")
        return []


def fetch_binance_perp_ticker_endpoint_data(symbols=None):
    base_url = BINANCE_PERP_TICKER_URL
    if symbols:
        base_url += format_request_parameters(symbols)
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Binance perp ticker data: {e}")
        send_telegram_log(f"Error connecting to binance perp: {e}")
        return []
    except ValueError as e:
        logger.error(f"Error parsing JSON response from Binance perp: {e}")
        return []

from datetime import datetime, timedelta

import requests

from core.common.constants import BINANCE_SPOT_KLINE_URL
from core.common.utils import send_telegram_log


def fetch_binance_klines_endpoint_data(symbol, days=30):
    current_date = datetime.now()
    current_date_ts = int(datetime.timestamp(current_date))
    days_ago = current_date - timedelta(days=days)
    days_ago_ts = int(datetime.timestamp(days_ago))

    parameters = {
        "symbol": symbol,
        "interval": "1d",
        "startTime": days_ago_ts * 1000,
        "endTime": current_date_ts * 1000,
    }
    try:
        response = requests.get(url=BINANCE_SPOT_KLINE_URL, params=parameters)
    except Exception as e:
        send_telegram_log(f"Error connecting to binance: {e}")
        return {}
    return response.json()

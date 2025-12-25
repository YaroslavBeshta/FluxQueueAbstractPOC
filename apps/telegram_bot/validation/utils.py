import lxml.html
import requests

from core.common.mappings import BINANCE_URL_MAPPING
from messages import message_with_args
from validation import error_messages


def validate_int_number(param):
    try:
        param = int(param)
        return None, param
    except ValueError:
        return error_messages.VALIDATE_INTEGER_ERROR, None


def validate_float_number(param):
    try:
        param = float(param)
        return None, param
    except ValueError:
        return error_messages.VALIDATE_FLOAT_ERROR, None


def validate_binance_market(market, market_type):
    base_url = BINANCE_URL_MAPPING[market_type]
    response = requests.get(f"{base_url}/ticker/24hr?symbol={market}")

    if response.status_code != 200:
        return message_with_args(error_messages.BINANCE_MARKET_EXISTANCE_ERROR, market)
    return None


def validate_yahoo_market(market):
    user_agent_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    url = f"https://finance.yahoo.com/quote/{market}"
    response = requests.get(url, headers=user_agent_headers)
    if response.status_code != 200:
        return message_with_args(error_messages.BINANCE_MARKET_EXISTANCE_ERROR, market)

    try:
        tree = lxml.html.fromstring(response.text)
        market_price = tree.xpath(
            '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')[0].text
    except Exception as e:
        return message_with_args(error_messages.BINANCE_MARKET_EXISTANCE_ERROR, market)
    return None
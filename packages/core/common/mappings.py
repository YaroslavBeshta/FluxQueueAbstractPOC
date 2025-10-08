from operator import ge, le

from core.common.constants import (BINANCE_PERP_URL, BINANCE_SPOT_URL,
                                       BINANCE_UI_PERP_URL,
                                       BINANCE_UI_SPOT_URL)

BINANCE_URL_MAPPING = {
    "spot": BINANCE_SPOT_URL,
    "perp": BINANCE_PERP_URL
}

BINANCE_UI_URL_MAPPING = {
    "spot": BINANCE_UI_SPOT_URL,
    "perp": BINANCE_UI_PERP_URL
}

MARKET_COMMAND_MAPPING = {
    "token": "spot",
    "tokenf": "perp",
    "market": "spot",
    "marketf": "perp"
}

INEQUALITY_SIGN_MAPPING = {
    "gt": ">",
    "lt": "&#60;",
    ">": "gt",
    "<": "lt"
}

INEQUALITY_OPERATOR_MAPPING = {
    "gt": ge,
    "lt": le
}

TICKER_MAPPING = {
    "DXY": "DX-Y.NYB",
    "S&P500": "^GSPC"
}

from markup.generator import build_keyboard
from message_generators import generate_market_digest_messages
from processors import process_binance_ticker_response
from sender import notify
from sources import fetch_binance_perp_ticker_endpoint_data
from utils import combine_market_token_digest


def generate_perp_market_notifications():
    notifications = {}

    ticker_data = fetch_binance_perp_ticker_endpoint_data()
    processed_data = process_binance_ticker_response(ticker_data)
    notifications = generate_market_digest_messages("perp", processed_data)
    notifications = combine_market_token_digest(notifications, market_type="perp")
    notify(notifications, build_keyboard("perp", "market"))

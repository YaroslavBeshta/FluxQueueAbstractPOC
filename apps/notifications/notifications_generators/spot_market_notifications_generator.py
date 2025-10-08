from markup.generator import build_keyboard
from message_generators import generate_market_digest_messages
from processors import process_binance_ticker_response
from sender import notify
from sources import fetch_binance_spot_ticker_endpoint_data
from utils import combine_market_token_digest


def generate_spot_market_notifications():
    notifications = {}

    spot_ticker_data = fetch_binance_spot_ticker_endpoint_data()
    processed_data = process_binance_ticker_response(spot_ticker_data)
    notifications = generate_market_digest_messages("spot", processed_data)
    notifications = combine_market_token_digest(notifications, market_type="spot")
    notify(notifications, build_keyboard("spot", "market"))

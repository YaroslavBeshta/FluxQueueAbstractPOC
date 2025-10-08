from markup.generator import build_keyboard
from message_generators import generate_token_digest_messages
from processors import process_binance_ticker_response
from sender import notify
from sources import fetch_binance_spot_ticker_endpoint_data


def generate_spot_token_notifications():
    spot_ticker_data = fetch_binance_spot_ticker_endpoint_data()
    processed_data = process_binance_ticker_response(spot_ticker_data)
    notifications = generate_token_digest_messages("spot", processed_data)
    notify(notifications, build_keyboard("spot", "token"))

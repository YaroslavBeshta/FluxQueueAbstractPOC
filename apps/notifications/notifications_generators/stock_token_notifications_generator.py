from core.models.management.subscriptions.token import get_tokens_by_market_type
from markup.generator import build_keyboard
from message_generators import generate_token_digest_messages
from sender import notify
from sources import fetch_yahoo_symbols


def generate_stock_token_notifications():
    tokens = get_tokens_by_market_type("stock")
    processed_data = fetch_yahoo_symbols([token.symbol for token in tokens])
    notifications = generate_token_digest_messages("stock", processed_data)
    notify(notifications, build_keyboard("stock", "token"))

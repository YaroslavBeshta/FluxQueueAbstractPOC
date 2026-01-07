from core.common.logger import get_logger
from core.common.mappings import INEQUALITY_OPERATOR_MAPPING
from core.common.utils import dict_upsert
from core.models.management.subscriptions.token import \
    get_token_subscriptions

logger = get_logger(__name__)


def generate_message(symbol, token_price, market_type):
    if market_type == "perp":
        market_type = "FUTURES"
    market_type = market_type.upper()
    return f"🔔 {symbol} price: {token_price} <b>[{market_type}]</b>"


def generate_token_digest_messages(market_type, processed_data):
    # Validate processed_data
    if not processed_data or not isinstance(processed_data, dict):
        logger.warning(f"No processed data available for {market_type} market")
        return {}
    
    subscriptions = get_token_subscriptions(market_type=market_type)

    notifications = {}
    for subscription in subscriptions:
        symbol = subscription.symbol
        
        # Check if symbol exists in processed_data
        # Symbols may be missing if they haven't had recent trading activity
        if symbol not in processed_data:
            logger.debug(f"Symbol {symbol} not found in {market_type} ticker data (may be inactive)")
            continue
        
        try:
            symbol_data = processed_data[symbol]
            if "last_price" not in symbol_data:
                logger.warning(f"Symbol {symbol} missing 'last_price' in processed data")
                continue
                
            token_price = float(symbol_data["last_price"])
            
            if INEQUALITY_OPERATOR_MAPPING[subscription.sign](
                token_price, subscription.price
            ):
                dict_upsert(
                    notifications,
                    str(subscription.telegram_id),
                    generate_message(symbol, token_price, market_type)
                )
        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Error processing subscription for {symbol}: {e}")
            continue
    
    return notifications

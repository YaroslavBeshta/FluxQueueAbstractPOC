import time

from core.common.logger import get_logger

logger = get_logger(__name__)


def process_binance_ticker_response(response):
    """
    Process Binance ticker response and filter for recently updated symbols.
    
    Args:
        response: List of ticker data from Binance API
        
    Returns:
        dict: Dictionary mapping symbol to price data, filtered to symbols
              updated in the last 60 seconds
    """
    if not response or not isinstance(response, list):
        logger.warning("Invalid or empty response from Binance API")
        return {}
    
    data = {}
    current_time_ms = int(time.time() * 1000)
    cutoff_time = current_time_ms - (60 * 1000)  # 60 seconds ago
    
    for row in response:
        try:
            # Validate required fields
            if not isinstance(row, dict):
                continue
            if "symbol" not in row or "closeTime" not in row:
                continue
            if "lastPrice" not in row or "priceChangePercent" not in row:
                continue
            
            # Only include symbols that were updated in the last 60 seconds
            if row["closeTime"] >= cutoff_time:
                data[row["symbol"]] = {
                    "price_change_percent": row["priceChangePercent"],
                    "last_price": row["lastPrice"]
                }
        except (KeyError, TypeError, ValueError) as e:
            logger.debug(f"Error processing ticker row: {e}")
            continue
    
    return data

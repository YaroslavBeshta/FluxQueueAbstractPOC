import time

def process_binance_ticker_response(response):
    data = {}
    for row in response:
        current_time_ms = int(time.time() * 1000)
        if current_time_ms - row["closeTime"] < (60 * 1000):
            data[row["symbol"]] = {
                "price_change_percent": row["priceChangePercent"],
                "last_price": row["lastPrice"]
            }
    return data

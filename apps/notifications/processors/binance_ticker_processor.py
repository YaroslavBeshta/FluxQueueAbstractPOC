def process_binance_ticker_response(response):
    data = {}
    for row in response:
        data[row["symbol"]] = {
            "price_change_percent": row["priceChangePercent"],
            "last_price": row["lastPrice"]
        }
    return data

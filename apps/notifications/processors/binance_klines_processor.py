import pandas as pd


def process_binance_klines_response(response):
    columns = [
        "kline_open_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "kline_close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "unused_field"
    ]
    df = pd.DataFrame(response, columns=columns).astype(
        {
            "high_price": float,
            "low_price": float,
            "volume": float,
        }
    )
    df["avg_price"] = (df["high_price"] + df["low_price"]) / 2

    days_ago_30 = df.iloc[0]
    days_ago_7 = df.iloc[-7]
    current_day = df.iloc[-1]

    # 7 days
    price_change_7 = current_day["avg_price"] - days_ago_7["avg_price"]
    price_change_percent_7 = price_change_7 / days_ago_7["avg_price"] * 100
    volume_change_7 = current_day["volume"] - days_ago_7["volume"]
    volume_change_percent_7 = volume_change_7 / days_ago_7["volume"] * 100

    # 30 days
    price_change_30 = current_day["avg_price"] - days_ago_30["avg_price"]
    price_change_percent_30 = price_change_30 / days_ago_30["avg_price"] * 100
    volume_change_30 = current_day["volume"] - days_ago_30["volume"]
    volume_change_percent_30 = volume_change_30 / days_ago_30["volume"] * 100

    # if median > mean - uptrend, otherwise downtrend
    mean = df["avg_price"].mean()
    median = df["avg_price"].median()

    return {
        "price_change_7": price_change_7,
        "price_change_percent_7": price_change_percent_7,
        "volume_change_7": volume_change_7,
        "volume_change_percent_7": volume_change_percent_7,

        "price_change_30": price_change_30,
        "price_change_percent_30": price_change_percent_30,
        "volume_change_30": volume_change_30,
        "volume_change_percent_30": volume_change_percent_30,

        "mean": mean,
        "median": median,

        "current_high": current_day["high_price"],
        "current_low": current_day["low_price"]
    }

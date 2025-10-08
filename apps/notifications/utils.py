def format_request_parameters(symbols):
    return "?symbols=[" + ",".join([f"%22{symbol}%22" for symbol in symbols]) + "]"


def combine_market_token_digest(notifications, market_type):
    if market_type == "perp":
        market_type = "futures"
    market_type = market_type.title()
    for chat_id, messages in notifications.items():
        final_message = f"<b>{market_type}</b> market impulse:\n\n"
        final_message += "\n".join(messages)
        notifications[chat_id] = [final_message]
    return notifications

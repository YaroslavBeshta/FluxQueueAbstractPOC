from markup import button_texts


def add_mute_buttons(market_type, subscription_type):
    return [
        {
            "text": button_texts.MUTE_1H,
            "callback_data": f"mute_{subscription_type}_{market_type}_1h"
        },
        {
            "text": button_texts.MUTE_24H,
            "callback_data": f"mute_{subscription_type}_{market_type}_24h"
        }
    ]


def add_unmute_unsub_buttons(market_type, subscription_type):
    return [
        {
            "text": button_texts.UNMUTE,
            "callback_data": f"unmute_{subscription_type}_{market_type}_"
        },
        {
            "text": button_texts.UNSUB,
            "callback_data": f"unsub_{subscription_type}_{market_type}_"
        },
    ]


def build_keyboard(market_type, subscription_type):
    markup = {"inline_keyboard": []}
    markup["inline_keyboard"].append(
        add_mute_buttons(market_type, subscription_type)
    )
    markup["inline_keyboard"].append(
        add_unmute_unsub_buttons(market_type, subscription_type)
    )
    return markup

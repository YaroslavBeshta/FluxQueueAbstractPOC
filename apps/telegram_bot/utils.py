from core.common.mappings import INEQUALITY_SIGN_MAPPING


def extract_parameter(command):
    command_text = command.split(" ")
    if len(command_text) >= 2:
        return command_text[1]
    return None


def parse_command_with_parameters(user_input):
    command, *parameters = user_input.split(" ")
    return command, *parameters


def enumerate_list_and_join(lst, delimiter="\n"):
    for i, elem in enumerate(lst):
        lst[i] = f"{i + 1}. {elem}"
    return delimiter.join(lst)


def divide_spot_and_perp(subscriptions):
    spot, perp, stock = [], [], []
    for subscription in subscriptions:
        if subscription.market_type == "spot":
            spot.append(subscription)
        if subscription.market_type == "perp":
            perp.append(subscription)
        if subscription.market_type == "stock":
            stock.append(subscription)
    return spot, perp, stock


def build_token_subscriptions_message(subscriptions, market_type):
    header = f"\n<b>[{market_type.upper()}]</b>\n"
    body = []
    for subscription in subscriptions:
        muted = ""
        if subscription.muted_1h_at or subscription.muted_24h_at:
            muted = "🔇"
        body.append(
            (
                f"{subscription.symbol}"
                f" {INEQUALITY_SIGN_MAPPING[subscription.sign]} "
                f"{subscription.price} {muted}"
            )
        )
    return header + enumerate_list_and_join(body) + "\n"


def build_market_subscriptions_message(subscriptions, market_type):
    header = f"\n<b>[{market_type.upper()}]</b>\n"
    body = []
    for subscription in subscriptions:
        muted = ""
        if subscription.muted_1h_at or subscription.muted_24h_at:
            muted = "🔇"
        body.append(
            (
                f" {INEQUALITY_SIGN_MAPPING[subscription.sign]} "
                f"{subscription.percent}% {muted}"
            )
        )
    return header + enumerate_list_and_join(body) + "\n"

from core.common.mappings import INEQUALITY_SIGN_MAPPING, MARKET_COMMAND_MAPPING
import messages
from utils import parse_command_with_parameters
from validation.utils import (
    validate_binance_market,
    validate_float_number,
    validate_int_number,
    validate_yahoo_market,
)


def token_command_input_validator(message):
    command, *parameters = parse_command_with_parameters(message)
    if not len(parameters):
        return messages.TOKEN_COMMAND_HELP, []

    market = sign = price = None
    try:
        market, sign, price, *_ = parameters
    except ValueError:
        parameters = parameters.pop()
        if ">" in parameters:
            market, price, *_ = parameters.split(">")
            sign = ">"
        if "<" in parameters:
            market, price, *_ = parameters.split("<")
            sign = "<"
    if market is None or sign is None or price is None:
        return messages.TOKEN_COMMAND_HELP, []
    sign = INEQUALITY_SIGN_MAPPING.get(sign)
    if not sign:
        return messages.TOKEN_COMMAND_HELP, []

    market = market.upper()
    market_type = MARKET_COMMAND_MAPPING[command[1:]]
    error_message = validate_binance_market(market, market_type)
    if error_message:
        error_message = validate_yahoo_market(market)
        if error_message:
            return error_message, []
        market_type = "stock"

    error_message, price = validate_float_number(price)
    if error_message:
        return error_message, []

    return None, (market, market_type, sign, price)


def market_command_input_validator(message):
    command, *parameters = parse_command_with_parameters(message)
    if not len(parameters):
        # TODO: create error message
        return messages.MARKET_COMMAND_HELP, []

    market_type = MARKET_COMMAND_MAPPING[command[1:]]

    percent, *_ = parameters
    error_message, percent = validate_int_number(percent)
    if error_message:
        return error_message, []

    # if percent < 50:
    #     return messages.MARKET_COMMAND_PERCENT_ERROR, []

    return None, (percent, market_type)


def delete_token_command_input_validator(message):
    command, *parameters = parse_command_with_parameters(message)
    if not len(parameters):
        return messages.DELETE_COMMAND_HELP, []

    return None, parameters[0]

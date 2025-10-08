import datetime
import time

import schedule

from core.models.management.subscriptions.market import unmute_market_subscriptions
from core.models.management.subscriptions.token import unmute_token_subscriptions
import notifications_generators


def main():
    schedule.every(1).minutes.do(
        notifications_generators.generate_spot_token_notifications
    )
    schedule.every(1).minutes.do(
        notifications_generators.generate_spot_market_notifications
    )
    schedule.every(1).minutes.do(
        notifications_generators.generate_perp_token_notifications
    )
    schedule.every(1).minutes.do(
        notifications_generators.generate_perp_market_notifications
    )
    schedule.every(1).minutes.do(
        notifications_generators.generate_stock_token_notifications
    )
    schedule.every(1).minutes.do(unmute_market_subscriptions)
    schedule.every(1).minutes.do(unmute_token_subscriptions)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

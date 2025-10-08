from core import session
from core.common.utils import send_telegram_log
from core.models import User


def get_or_create_user_from_message(message) -> None:
    query = session.query(User)
    query = query.filter(User.telegram_id == message.from_user.id)
    tg_user = query.first()

    if tg_user:
        return

    tg_user = User(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot,
        is_premium=message.from_user.is_premium,
    )

    try:
        session.add(tg_user)
        session.commit()
    except Exception as e:
        send_telegram_log(e)
    finally:
        session.close()

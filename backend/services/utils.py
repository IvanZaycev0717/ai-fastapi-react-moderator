from datetime import datetime

import pytz

from settings import TIMEZONE


def get_current_date() -> datetime:
    """Возвращает дату и время в текущий момент."""
    return datetime.now(pytz.timezone(TIMEZONE))

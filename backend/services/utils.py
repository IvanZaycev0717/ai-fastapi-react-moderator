from datetime import datetime

import pytz

from settings import MAX_COMMENT_LENGTH, MIN_COMMENT_LENGTH, TIMEZONE


def get_current_date() -> datetime:
    """Возвращает дату и время в текущий момент."""
    return datetime.now(pytz.timezone(TIMEZONE))


def is_text_valid(text) -> bool:
    """Проверяет валиден ли текст, который ввёл пользователь."""
    if not isinstance(text, str):
        return False
    if len(text) < MIN_COMMENT_LENGTH or len(text) > MAX_COMMENT_LENGTH:
        return False
    return True

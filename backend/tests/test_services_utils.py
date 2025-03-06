from datetime import datetime

import pytz

from services.utils import get_current_date
from settings import TIMEZONE


def test_get_current_date():
    current_date = get_current_date()
    assert isinstance(current_date, datetime)
    assert current_date.tzinfo.zone == pytz.timezone(TIMEZONE).zone
    assert current_date <= datetime.now(pytz.timezone(TIMEZONE))

from datetime import datetime

import pytest
import pytz

from services.utils import compare_comments, get_current_date
from settings import TIMEZONE


def test_get_current_date():
    current_date = get_current_date()
    assert isinstance(current_date, datetime)
    assert current_date.tzinfo.zone == pytz.timezone(TIMEZONE).zone
    assert current_date <= datetime.now(pytz.timezone(TIMEZONE))


@pytest.mark.parametrize(
        ('old', 'new', 'result'),
        [('Abcd', 'Abcd', False),
         ('abcd', 'abCd', True)])
def test_compare_comments(old: str, new: str, result: bool):
    assert compare_comments(old, new) is result

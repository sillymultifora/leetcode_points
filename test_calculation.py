from datetime import datetime, timedelta
import pytest

from main import get_final_date
from dataclasses import dataclass


def test_one_day():
    date = datetime(year=2025, month=2, day=1)
    assert get_final_date(date, 0, 11, True, True, True) == date + timedelta(days=1)


@pytest.mark.parametrize("weeks", [1, 2])
def test_weeks(weeks):
    days_in_week = 7
    days = days_in_week * weeks
    week_points = 11 * days + 10 * weeks
    date = datetime(year=2025, month=1, day=1)
    assert get_final_date(
        date, 0, week_points, False, False, False
    ) == date + timedelta(days=days)


@dataclass
class TestSuit:
    start_data: datetime
    target: int
    is_biweekly: bool
    is_weekly: bool
    is_weekly_premium: bool
    reference: datetime


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=25),
            25 + 11,
            False,
            False,
            False,
            datetime(year=2025, month=1, day=26),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1),
            456,
            False,
            False,
            False,
            datetime(year=2025, month=2, day=1),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1),
            466,
            True,
            False,
            False,
            datetime(year=2025, month=2, day=1),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1),
            641,
            True,
            False,
            True,
            datetime(year=2025, month=2, day=1),
        ),  # Fails, because of the premium weekly
        TestSuit(
            datetime(year=2025, month=3, day=31),
            526,
            True,
            False,
            False,
            datetime(year=2025, month=5, day=1),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31),
            1457,
            True,
            False,
            False,
            datetime(year=2025, month=7, day=1),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31),
            616,
            True,
            True,
            False,
            datetime(year=2025, month=5, day=1),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31),
            1172,
            True,
            True,
            False,
            datetime(year=2025, month=6, day=1),
        ),
    ],
)
def test_reference(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            0,
            test_suit.target,
            test_suit.is_biweekly,
            test_suit.is_weekly,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )


def test_is_beweekly(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            0,
            test_suit.target,
            True,
            test_suit.is_weekly,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )

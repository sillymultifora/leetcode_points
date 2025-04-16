"""Tests for the LeetCode points calculator module."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest

from main import (
    BIWEEKLY_START_DATE,
    WEEKLY_START_DATE,
    add_two_weeks,
    get_final_date,
    next_check_in_30_day_streak_date,
    next_premium_weekly_date,
)


def test_one_day():
    date = datetime(year=2025, month=2, day=1, tzinfo=timezone.utc)
    assert get_final_date(date, 11, 0, True, True, True) == date + timedelta(days=1)


@pytest.mark.parametrize("weeks", [1, 2])
def test_weeks(weeks):
    days_in_week = 7
    days = days_in_week * weeks
    week_points = 11 * days + 10 * weeks
    date = datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    assert get_final_date(
        date, week_points, 0, False, False, False
    ) == date + timedelta(days=days)


@dataclass
class TestSuit:
    start_data: datetime
    target: int
    reference: datetime
    is_biweekly: bool = False
    is_weekly: bool = False
    is_weekly_premium: bool = False
    streak: int = 0


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=25, tzinfo=timezone.utc),
            11,  # no month awards
            datetime(year=2025, month=1, day=26, tzinfo=timezone.utc),
            False,
            False,
            False,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            456,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            False,
            False,
            False,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            641,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            True,
            False,
            True,
        ),
    ],
)
def test_reference(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            test_suit.target,
            0,
            test_suit.is_biweekly,
            test_suit.is_weekly,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            466,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=timezone.utc),
            526 - 50,  # no month award for the first month
            datetime(year=2025, month=5, day=1, tzinfo=timezone.utc),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=timezone.utc),
            1457 - 50 + 30 * 3,  # no month award for the first month
            datetime(year=2025, month=7, day=1, tzinfo=timezone.utc),
        ),
    ],
)
def test_is_beweekly(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            test_suit.target,
            0,
            True,
            test_suit.is_weekly,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=timezone.utc),
            616 - 50,  # no month award for the first month
            datetime(year=2025, month=5, day=1, tzinfo=timezone.utc),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=timezone.utc),
            1172 - 50,  # no month award for the first month
            datetime(year=2025, month=6, day=1, tzinfo=timezone.utc),
        ),
    ],
)
def test_is_beweekly_and_weekly(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            test_suit.target,
            0,
            True,
            True,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )


def test_date_before_2025_01_01():
    date = datetime(year=2024, month=12, day=31, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        get_final_date(date, 11, 0, True, True, True)


def test_date_matching_biweekly_date():
    date = BIWEEKLY_START_DATE
    assert get_final_date(date, 16, 0, True, False, False) == date + timedelta(days=1)


def test_date_matching_weekly_date():
    date = WEEKLY_START_DATE
    assert get_final_date(date, 16, 0, False, True, False) == date + timedelta(days=1)


def test_date_matching_only_weekly():
    date = WEEKLY_START_DATE
    assert get_final_date(date, 16, 0, True, True, False) == date + timedelta(days=1)


def test_date_matching_weekly_and_biweekly_date():
    biweekly_date = add_two_weeks(BIWEEKLY_START_DATE)
    target = (
        11 * 2 + 5 * 2 + 35
    )  # 2 days of daily + 2 contests participation + 35 days of join two contest
    assert get_final_date(
        biweekly_date, target, 0, True, True, False
    ) == biweekly_date + timedelta(days=2)


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            631,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=timezone.utc),
            11 + 35,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=timezone.utc),
            11,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            streak=1,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=timezone.utc),
            11 + 35 + 35 + 11,
            datetime(year=2025, month=2, day=2, tzinfo=timezone.utc),
        ),
    ],
)
def test_date_is_weekly_premium(test_suit):
    assert (
        get_final_date(
            test_suit.start_data, test_suit.target, test_suit.streak, False, False, True
        )
        == test_suit.reference
    )


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            651,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            is_weekly=True,
            is_weekly_premium=True,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=15, tzinfo=timezone.utc),
            11 * (31 - 14) + 35 * 3 + 10 * 2 + 2 * 5,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            is_weekly=True,
            is_weekly_premium=True,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=timezone.utc),
            651 + 35 * 2 + 5 * 2,
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            is_weekly=True,
            is_weekly_premium=True,
            is_biweekly=True,
        ),
    ],
)
def test_date_is_weekly_premium_and_contests(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            test_suit.target,
            test_suit.streak,
            test_suit.is_biweekly,
            test_suit.is_weekly,
            test_suit.is_weekly_premium,
        )
        == test_suit.reference
    )


def test_monday_luck_bonus():
    # Test starting on a Monday
    monday = datetime(
        year=2025, month=1, day=6, tzinfo=timezone.utc
    )  # This is a Monday
    target = 11 + 5  # Daily points + Monday luck bonus
    assert get_final_date(monday, target, 0, False, False, False) == monday + timedelta(
        days=1
    )

    # Test starting on a Sunday (next day should be Monday)
    sunday = datetime(
        year=2025, month=1, day=5, tzinfo=timezone.utc
    )  # This is a Sunday
    target = 11 * 2 + 5  # Two days of daily points + Monday luck bonus
    assert get_final_date(sunday, target, 0, False, False, False) == sunday + timedelta(
        days=2
    )


@pytest.mark.parametrize(
    "test_suit",
    [
        TestSuit(
            datetime(year=2025, month=1, day=25, tzinfo=timezone.utc),
            11 + 25,  # Daily points + 25 days streak bonus
            datetime(year=2025, month=1, day=26, tzinfo=timezone.utc),
            streak=25,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=timezone.utc),
            11 + 50,  # Daily points + month streak bonus
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            streak=31,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=25, tzinfo=timezone.utc),
            11 * 7
            + 10
            + 25
            + 50,  # Daily points + Monday luck + 25 days streak + month streak
            datetime(year=2025, month=2, day=1, tzinfo=timezone.utc),
            streak=25,
        ),
    ],
)
def test_month_streak_bonuses(test_suit):
    assert (
        get_final_date(
            test_suit.start_data,
            test_suit.target,
            test_suit.streak,
            False,
            False,
            False,
        )
        == test_suit.reference
    )


def test_invalid_streak():
    date = datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        get_final_date(date, 11, -1, False, False, False)  # Negative streak


def test_month_transition_edge_cases():
    # Test transition from 30-day month to 31-day month
    date = datetime(year=2025, month=4, day=30, tzinfo=timezone.utc)
    target = 11 + 50  # Daily points + month streak bonus
    assert get_final_date(date, target, 30, False, False, False) == date + timedelta(
        days=1
    )

    # Test transition from 31-day month to 30-day month
    date = datetime(year=2025, month=1, day=31, tzinfo=timezone.utc)
    target = 11 + 50  # Daily points + month streak bonus
    assert get_final_date(date, target, 31, False, False, False) == date + timedelta(
        days=1
    )


def test_next_premium_weekly_date():
    # Test within same month
    date = datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    next_date = next_premium_weekly_date(date)
    assert next_date == datetime(year=2025, month=1, day=8, tzinfo=timezone.utc)

    # Test month transition
    date = datetime(year=2025, month=1, day=29, tzinfo=timezone.utc)
    next_date = next_premium_weekly_date(date)
    assert next_date == datetime(year=2025, month=2, day=1, tzinfo=timezone.utc)

    # Test end of month
    date = datetime(year=2025, month=1, day=31, tzinfo=timezone.utc)
    next_date = next_premium_weekly_date(date)
    assert next_date == datetime(year=2025, month=2, day=1, tzinfo=timezone.utc)


def test_next_check_in_30_day_streak_date():
    date = datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    next_date = next_check_in_30_day_streak_date(date)
    assert next_date == datetime(year=2025, month=1, day=31, tzinfo=timezone.utc)

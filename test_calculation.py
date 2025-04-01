"""Tests for the LeetCode points calculator module."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import pytest

from main import (
    BIWEEKLY_START_DATE,
    WEEKLY_START_DATE,
    get_final_date,
    next_biweekly_date,
)


def test_one_day():
    date = datetime(year=2025, month=2, day=1, tzinfo=UTC)
    assert get_final_date(date, 11, 0, True, True, True) == date + timedelta(days=1)


@pytest.mark.parametrize("weeks", [1, 2])
def test_weeks(weeks):
    days_in_week = 7
    days = days_in_week * weeks
    week_points = 11 * days + 10 * weeks
    date = datetime(year=2025, month=1, day=1, tzinfo=UTC)
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
            datetime(year=2025, month=1, day=25, tzinfo=UTC),
            11,  # no month awards
            datetime(year=2025, month=1, day=26, tzinfo=UTC),
            False,
            False,
            False,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=UTC),
            456,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
            False,
            False,
            False,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=1, tzinfo=UTC),
            641,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
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
            datetime(year=2025, month=1, day=1, tzinfo=UTC),
            466,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=UTC),
            526 - 50,  # no month award for the first month
            datetime(year=2025, month=5, day=1, tzinfo=UTC),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=UTC),
            1457 - 50,  # no month award for the first month
            datetime(year=2025, month=7, day=1, tzinfo=UTC),
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
            datetime(year=2025, month=3, day=31, tzinfo=UTC),
            616 - 50,  # no month award for the first month
            datetime(year=2025, month=5, day=1, tzinfo=UTC),
        ),
        TestSuit(
            datetime(year=2025, month=3, day=31, tzinfo=UTC),
            1172 - 50,  # no month award for the first month
            datetime(year=2025, month=6, day=1, tzinfo=UTC),
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
    date = datetime(year=2024, month=12, day=31, tzinfo=UTC)
    with pytest.raises(ValueError):
        get_final_date(date, 11, 0, True, True, True)


def test_date_matching_biweekly_date():
    date = BIWEEKLY_START_DATE
    assert get_final_date(date, 16, 0, True, False, False) == date + timedelta(days=1)


def test_date_matching_weekly_date():
    date = WEEKLY_START_DATE
    assert get_final_date(date, 16, 0, False, True, False) == date + timedelta(days=1)


def test_date_not_matching_weekly_and_biweekly_date():
    date = WEEKLY_START_DATE
    assert get_final_date(date, 16, 0, True, True, False) == date + timedelta(days=1)


def test_date_matching_weekly_and_biweekly_date():
    biweekly_date = next_biweekly_date(BIWEEKLY_START_DATE)
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
            datetime(year=2025, month=1, day=1, tzinfo=UTC),
            631,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=UTC),
            11 + 35,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=UTC),
            11,
            datetime(year=2025, month=2, day=1, tzinfo=UTC),
            streak=1,
        ),
        TestSuit(
            datetime(year=2025, month=1, day=31, tzinfo=UTC),
            11 + 35 + 35 + 11,
            datetime(year=2025, month=2, day=2, tzinfo=UTC),
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


# TODO: add test for is_weekly_premium, and is_weekly_premium and is_weekly/is_biweekly

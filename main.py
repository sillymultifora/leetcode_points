"""LeetCode points calculator to determine when you'll reach your target points."""

import calendar
from argparse import ArgumentParser
from datetime import datetime, timedelta, timezone

# LC Points constants
DAILY = 11
TWENTY_FIVE_DAYS = 25
MONTH = 50
CONTEST = 5
JOIN_TWO_CONTEST = 35
PREMIUM_WEEKLY = 35
MONDAY_LUCK = 10
# LC Date constants
BIWEEKLY_START_DATE = datetime(2025, 1, 4, tzinfo=timezone.utc)
WEEKLY_START_DATE = datetime(2025, 1, 5, tzinfo=timezone.utc)


def add_one_week(day: datetime) -> datetime:
    """Add one week to the given date."""
    return day + timedelta(days=7)


def add_two_weeks(day: datetime) -> datetime:
    """Add two weeks to the given date."""
    return add_one_week(add_one_week(day))


def next_premium_weekly_date(date: datetime) -> datetime:
    """Calculate the next premium weekly problem date."""
    weekly_premium_date = add_one_week(date)
    if weekly_premium_date.month != date.month:  # First day of a month
        weekly_premium_date = datetime.replace(weekly_premium_date, day=1)
    return weekly_premium_date


def is_current_month_fully_solved_till_today(date: datetime, streak: int) -> bool:
    """Check if all problems in the current month up to today are solved."""
    start_month = datetime(date.year, date.month, day=1, tzinfo=timezone.utc)
    return date - timedelta(days=streak) <= start_month


def check_date(date: datetime) -> None:
    """Validate the input date meets the requirements."""
    min_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    if date < min_date:
        raise ValueError(f"Date should start from 2025 year, but got {date}")
    if date.hour != 0 or date.minute != 0 or date.second != 0 or date.microsecond != 0:
        raise ValueError(
            "Date should not contain hours, minutes, seconds or microseconds"
        )


def check_streak(streak: int) -> None:
    """Validate the streak count is non-negative."""
    if streak < 0:
        raise ValueError("Streak should be non-negative.")


def get_final_date(
    date: datetime,
    target: int,
    streak: int,
    is_biweekly: bool,
    is_weekly: bool,
    is_weekly_premium: bool,
) -> datetime:
    """Calculate the date when the target points will be reached."""
    check_date(date)
    check_streak(streak)

    current = 0
    biweekly_date = BIWEEKLY_START_DATE
    weekly_date = WEEKLY_START_DATE
    weekly_premium_date = datetime(date.year, date.month, day=1, tzinfo=timezone.utc)

    is_month_streak_active = is_current_month_fully_solved_till_today(date, streak)

    while date > biweekly_date:
        biweekly_date = add_two_weeks(biweekly_date)
    while date > weekly_date:
        weekly_date = add_one_week(weekly_date)
    while date > weekly_premium_date:
        weekly_premium_date = next_premium_weekly_date(weekly_premium_date)

    if is_weekly_premium and weekly_premium_date > date and streak == 0:
        current += PREMIUM_WEEKLY  # count current weekly_premium

    while current < target:
        end_day = calendar.monthrange(date.year, date.month)[1]
        current += DAILY
        if date.day == 25 and is_month_streak_active:
            current += TWENTY_FIVE_DAYS
        if calendar.weekday(date.year, date.month, date.day) == calendar.MONDAY:
            current += MONDAY_LUCK
        if is_weekly_premium and date == weekly_premium_date:
            current += PREMIUM_WEEKLY
            weekly_premium_date = next_premium_weekly_date(weekly_premium_date)
        if is_biweekly and date == biweekly_date:
            current += CONTEST
            if (
                is_weekly
                and biweekly_date.isocalendar().week == weekly_date.isocalendar().week
            ):
                current += JOIN_TWO_CONTEST
            biweekly_date = add_two_weeks(biweekly_date)
        if is_weekly and date == weekly_date:
            weekly_date = add_one_week(weekly_date)
            current += CONTEST
        if date.day == end_day and is_month_streak_active:
            current += MONTH
        date = date + timedelta(days=1)
        if date.day == 1:
            is_month_streak_active = True
    return date


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("current", type=int, help="Number of points you have.")
    parser.add_argument(
        "target",
        type=int,
        nargs="?",
        default=7200,
        help="Target number of points to achieve (default: 7200).",
    )
    parser.add_argument(
        "streak",
        type=int,
        nargs="?",
        default=0,
        help="Current number of streak days.",
    )
    parser.add_argument(
        "--today-collected",
        action="store_true",
        help="Flag indicating you have already collected today's points.",
    )
    parser.add_argument(
        "--biweekly-contest",
        action="store_true",
        help="Flag indicating you participate in every biweekly contest.",
    )
    parser.add_argument(
        "--weekly-contest",
        action="store_true",
        help="Flag indicating you participate in every weekly contest.",
    )
    parser.add_argument(
        "--weekly-premium",
        action="store_true",
        help="Flag indicating you solve premium weekly LeetCode problems.",
    )

    args = parser.parse_args()

    utc_dt = datetime.now(timezone.utc)
    # we care only about days
    utc_dt = utc_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if args.today_collected:
        utc_dt = utc_dt + timedelta(days=1)

    final_date = get_final_date(
        utc_dt,
        args.target - args.current,
        args.streak,
        args.biweekly_contest,
        args.weekly_contest,
        args.weekly_premium,
    )
    msg = f"You will reach your target on {final_date}"
    print(msg)

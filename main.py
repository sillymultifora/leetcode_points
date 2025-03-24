import calendar
from argparse import ArgumentParser
from datetime import datetime, timedelta

# LC Points constants
DAILY = 11
TWENTY_FIVE_DAYS = 25
MONTH = 50
CONTEST = 5
JOIN_TWO_CONTEST = 35
PREMIUM_WEEKLY = 35
MONDAY_LUCK = 10
# LC Date constants
BIWEEKLY_START_DATE = datetime(
    2025, 3, 15, 0, 0
)  #  original with hours and minutes: datetime(2025, 3, 15, 15, 30)
WEEKLY_START_DATE = datetime(
    2025, 3, 16, 0, 0
)  #  original with hours and minutes: datetime(2025, 3, 15, 3, 30)


def next_biweekly_date(day: datetime) -> datetime:
    return day + timedelta(days=14)


def next_weekly_date(day: datetime) -> datetime:
    return day + timedelta(days=7)


def get_final_date(
    date: datetime,
    current: int,
    target: int,
    is_biweekly: bool,
    is_weekly: bool,
    is_weekly_premium: bool,
) -> datetime:
    biweekly_date = BIWEEKLY_START_DATE
    weekly_date = WEEKLY_START_DATE
    while date > biweekly_date:
        biweekly_date = next_biweekly_date(biweekly_date)
    while date > weekly_date:
        weekly_date = next_weekly_date(weekly_date)
    while current < target:
        end_day = calendar.monthrange(date.year, date.month)[1]
        current += DAILY
        if date.day == 25:
            current += TWENTY_FIVE_DAYS
        if calendar.weekday(date.year, date.month, date.day) == calendar.MONDAY:
            current += MONDAY_LUCK
        if (
            is_weekly_premium
            and calendar.weekday(date.year, date.month, date.day) == calendar.SATURDAY
        ):
            current += PREMIUM_WEEKLY
        if is_biweekly and date == biweekly_date:
            current += CONTEST
            if (
                is_weekly
                and biweekly_date.isocalendar().week == weekly_date.isocalendar().week
            ):
                current += JOIN_TWO_CONTEST
            biweekly_date = next_biweekly_date(biweekly_date)
        if is_weekly and date == weekly_date:
            weekly_date = next_weekly_date(weekly_date)
            current += CONTEST
        if date.day == end_day:
            current += MONTH
        date = date + timedelta(days=1)
    return date


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "current", type=int, help="Current number of points you already have."
    )
    parser.add_argument(
        "target",
        type=int,
        nargs="?",
        default=7200,
        help="Target number of points to achieve (default: 7200).",
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

    utc_dt = datetime.utcnow()
    if args.today_collected:
        utc_dt += timedelta(days=1)
    utc_dt = utc_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    final_date = get_final_date(
        utc_dt,
        args.current,
        args.target,
        args.biweekly_contest,
        args.weekly_contest,
        args.weekly_premium,
    )
    print(final_date)

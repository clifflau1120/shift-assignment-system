"""Module of date time utilities."""

import typing
from datetime import date, timedelta

import more_itertools

EPOCH = date(1970, 1, 1)


def date_range(start_date: date, end_date: date) -> typing.Generator[date, None, None]:
    """Yield all the `date`s between a date range."""

    current_date = start_date

    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def count_n_date_sequences(n: int, dates: list[date]) -> int:
    """
    Count the number of non-overlapping date sequences of length `n`.

    Args:
        n (int): the number of consecutive dates per group
        dates (list[date]): a list of dates
    """

    def days_since_epoch(date_: date) -> int:
        return (date_ - EPOCH).days

    return sum(
        more_itertools.ilen(consecutive_dates) // n
        for consecutive_dates in more_itertools.consecutive_groups(dates, ordering=days_since_epoch)
    )

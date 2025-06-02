"""Module of `ConsecutiveNightShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class ConsecutiveNightShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that:

    1. Limits the number of consecutive night shifts
    2. Ensures consecutive night shifts are followed by at least two days of rest
    """

    def add_hard_constraints(self) -> None:
        self._limit_consecutive_night_shifts()
        self._ensure_consecutive_night_shifts_are_followed_by_two_days_of_rest()

    def _limit_consecutive_night_shifts(self) -> None:
        for worker, consecutive_dates in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(
                self._config.period,
                constants.MAX_CONSECUTIVE_NIGHT_SHIFTS + 1,
            ),
        ):
            total_night_shifts = sum(
                self._shift_assignments.get(worker, types.Shift.NIGHT, scheduled_date)
                for scheduled_date in consecutive_dates
            )

            self._model.add(total_night_shifts <= constants.MAX_CONSECUTIVE_NIGHT_SHIFTS)

    def _ensure_consecutive_night_shifts_are_followed_by_two_days_of_rest(self) -> None:
        for worker, (day_1, day_2, day_3, day_4) in itertools.product(
            self._config.full_time_workers,
            more_itertools.sliding_window(self._config.period, 4),
        ):
            consecutive_night_shifts = [
                self._shift_assignments.get(worker, types.Shift.NIGHT, day_1),
                self._shift_assignments.get(worker, types.Shift.NIGHT, day_2),
            ]

            total_rests = sum(
                self._shift_assignments.get(worker, shift, day)
                for shift, day in itertools.product(
                    types.Shift.all_resting_shifts(), (day_3, day_4)
                )
            )

            self._model.add(total_rests == 2).only_enforce_if(*consecutive_night_shifts)

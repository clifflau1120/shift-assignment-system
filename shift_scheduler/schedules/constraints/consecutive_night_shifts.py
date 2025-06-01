"""Module of `ConsecutiveNightShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class ConsecutiveNightShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures
    there will only be at most a certain number of consecutive night shifts.
    """

    def add_hard_constraints(self) -> None:
        for worker, consecutive_dates in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(
                self._config.period,
                constants.MAX_CONSECUTIVE_NIGHT_SHIFTS + 1,
            ),
        ):
            total_time_offs = sum(
                self._shift_assignments.get(worker, types.Shift.NIGHT, scheduled_date)
                for scheduled_date in consecutive_dates
            )

            self._model.add(total_time_offs <= constants.MAX_CONSECUTIVE_NIGHT_SHIFTS)

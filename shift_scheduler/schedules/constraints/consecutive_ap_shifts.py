"""Module of `ConsecutiveApShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class ConsecutiveApShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures
    there will only be at most a certain number of consecutive morning/afternoon shifts.
    """

    def add_hard_constraints(self) -> None:
        for worker, consecutive_dates in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(
                self._config.period,
                constants.MAX_CONSECUTIVE_AP_SHIFTS + 1,
            ),
        ):
            total_working_days = sum(
                self._shift_assignments.get(worker, shift, scheduled_date)
                for shift, scheduled_date in itertools.product(
                    types.Shift.all_morning_shifts() & types.Shift.all_afternoon_shifts(),
                    consecutive_dates,
                )
            )

            self._model.add(total_working_days <= constants.MAX_CONSECUTIVE_AP_SHIFTS)

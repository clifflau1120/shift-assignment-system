"""Module of `DailyAssignmentConstraint`."""

import itertools

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class DailyAssignmentConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures each worker has exactly one shift assignment per day.
    """

    def add_hard_constraints(self) -> None:
        for worker, scheduled_date in itertools.product(
            self._config.full_time_workers,
            self._config.period,
        ):
            shift_assignments_per_date = (
                self._shift_assignments.get(worker, shift, scheduled_date) for shift in types.Shift
            )
            self._model.add_exactly_one(shift_assignments_per_date)

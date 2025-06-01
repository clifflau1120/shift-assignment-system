"""Module of `SpecialWorkingShiftConstraint`."""

import itertools

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class SpecialWorkingShiftConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that penalizes assignments of special working shifts.
    """

    def create_soft_constraints(self) -> base.PenaltyExpression:
        special_working_shifts = sum(
            self._shift_assignments.get(worker, shift, scheduled_date)
            for worker, shift, scheduled_date in itertools.product(
                self._config.all_workers,
                types.Shift.special_working_shifts(),
                self._config.period,
            )
        )

        return special_working_shifts * self._penalty_per_unit

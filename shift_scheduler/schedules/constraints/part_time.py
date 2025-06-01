"""Module of `PartTimeAssignmentConstraint`."""

import itertools

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class PartTimeAssignmentConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that penalizes shift assignments for part-time workers.
    """

    def create_soft_constraints(self) -> base.PenaltyExpression:
        part_time_assignments = sum(
            self._shift_assignments.get(worker, shift, scheduled_date)
            for worker, shift, scheduled_date in itertools.product(
                self._config.part_time_workers,
                types.Shift,
                self._config.period,
            )
        )

        return part_time_assignments * self._penalty_per_unit

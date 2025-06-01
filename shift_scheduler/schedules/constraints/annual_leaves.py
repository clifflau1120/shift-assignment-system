"""Module of `AnnualLeavesConstraint`."""

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class AnnualLeavesConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures annual leaves can only be assigned on request.
    """

    def add_hard_constraints(self) -> None:
        for worker, preference in self._config.workers.items():
            annual_leaves = preference.requests.get(types.Shift.ANNUAL_LEAVE) or set()

            for scheduled_date in self._config.period:
                shift_assignment = self._shift_assignments.get(
                    worker,
                    types.Shift.ANNUAL_LEAVE,
                    scheduled_date,
                )

                is_annual_leave = scheduled_date in annual_leaves

                self._model.add(shift_assignment == int(is_annual_leave))

"""Module of `BirthdayLeaveConstraint`."""

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class BirthdayLeaveConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures birthday leaves can only be assigned on request.
    """

    def add_hard_constraints(self) -> None:
        for worker, preference in self._config.workers.items():
            birthday_leaves = preference.requests.get(types.Shift.BIRTHDAY_LEAVE) or set()

            for scheduled_date in self._config.period:
                shift_assignment = self._shift_assignments.get(
                    worker,
                    types.Shift.BIRTHDAY_LEAVE,
                    scheduled_date,
                )

                is_birthday_leave = scheduled_date in birthday_leaves

                self._model.add(shift_assignment == int(is_birthday_leave))

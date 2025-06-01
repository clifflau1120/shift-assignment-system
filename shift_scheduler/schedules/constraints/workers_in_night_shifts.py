"""Module of `NightShiftConstraint`."""

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class NightShiftConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures a certain number of workers every night.
    """

    def add_hard_constraints(self) -> None:
        for scheduled_date in self._config.period:
            total_workers_at_night = sum(
                self._shift_assignments.get(worker, types.Shift.NIGHT, scheduled_date)
                for worker in self._config.all_workers
            )

            self._model.add(total_workers_at_night == constants.NUM_WORKERS_AT_NIGHT)

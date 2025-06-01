"""Module of `TimeOffConstraint`."""

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class TimeOffConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures a certain number of time offs per worker.
    """

    def add_hard_constraints(self) -> None:
        for worker in self._config.full_time_workers:
            total_time_offs = sum(
                self._shift_assignments.get(worker, types.Shift.TIME_OFF, scheduled_date)
                for scheduled_date in self._config.period
            )

            self._model.add(total_time_offs >= constants.MIN_TIME_OFFS)
            self._model.add(total_time_offs <= constants.MAX_TIME_OFFS)

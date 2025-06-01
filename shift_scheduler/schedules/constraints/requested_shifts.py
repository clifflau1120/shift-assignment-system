"""Module of `RequestedShiftsConstraint`."""

from shift_scheduler.schedules.constraints import base


class RequestedShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures requests shifts are assigned.
    """

    def add_hard_constraints(self) -> None:
        for worker, preference in self._config.workers.items():
            for shift, requested_dates in preference.requests.items():
                for requested_date in requested_dates:
                    requested_shift = self._shift_assignments.get(worker, shift, requested_date)
                    self._model.add_exactly_one(requested_shift)

"""Module of `AfterNightShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class AfterNightShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures
    a night shift is always followed by a time-off or another night shift.
    """

    def add_hard_constraints(self) -> None:
        for worker, (today, tomorrow) in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(self._config.period, 2),
        ):
            night_shift_today = self._shift_assignments.get(worker, types.Shift.NIGHT, today)

            night_shift_tomorrow = self._shift_assignments.get(worker, types.Shift.NIGHT, tomorrow)
            time_off_tomorrow = self._shift_assignments.get(worker, types.Shift.TIME_OFF, tomorrow)

            self._model.add_bool_or(
                night_shift_tomorrow,
                time_off_tomorrow,
            ).only_enforce_if(night_shift_today)

"""Module of `AfterAfternoonShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class AfterAfternoonShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that represents:

    - Hard constraint: respects workers who do not accept a morning shift after an afternoon shift
    - Soft constraint: penalizes schedules when workers have PA shifts
    """

    def add_hard_constraints(self) -> None:
        for (worker, preference), (today, tomorrow) in itertools.product(
            self._config.workers.items(),
            more_itertools.sliding_window(self._config.period, 2),
        ):
            if not preference.accept_pa_shifts:
                afternoon_shift_today = sum(
                    self._shift_assignments.get(worker, shift, today)
                    for shift in types.Shift.all_afternoon_shifts()
                )

                morning_shift_tomorrow = sum(
                    self._shift_assignments.get(worker, shift, tomorrow)
                    for shift in types.Shift.all_morning_shifts()
                )

                self._model.add(afternoon_shift_today + morning_shift_tomorrow <= 1)

    def create_soft_constraints(self) -> base.PenaltyExpression:
        penalty: base.PenaltyExpression = 0

        for worker, (today, tomorrow) in itertools.product(
            self._config.workers,
            more_itertools.sliding_window(self._config.period, 2),
        ):
            afternoon_shift_today = sum(
                self._shift_assignments.get(worker, shift, today)
                for shift in types.Shift.all_afternoon_shifts()
            )

            morning_shift_tomorrow = sum(
                self._shift_assignments.get(worker, shift, tomorrow)
                for shift in types.Shift.all_morning_shifts()
            )

            should_penalize = self._model.new_bool_var("")
            self._model.add((afternoon_shift_today + morning_shift_tomorrow) >= 2).only_enforce_if(
                should_penalize
            )
            self._model.add((afternoon_shift_today + morning_shift_tomorrow) < 2).only_enforce_if(
                ~should_penalize
            )

            penalty += should_penalize * self._penalty_per_unit

        return penalty

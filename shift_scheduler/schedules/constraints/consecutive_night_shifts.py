"""Module of `ConsecutiveNightShiftsConstraint`."""

import itertools

import more_itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base


class ConsecutiveNightShiftsConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that represents:

    - Hard constraint: ensures at most a certain number of consecutive night shifts
    - Soft constraint: penalizes conescutive night shifts without two time-offs
    """

    def add_hard_constraints(self) -> None:
        for worker, consecutive_dates in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(
                self._config.period,
                constants.MAX_CONSECUTIVE_NIGHT_SHIFTS + 1,
            ),
        ):
            total_night_shifts = sum(
                self._shift_assignments.get(worker, types.Shift.NIGHT, scheduled_date)
                for scheduled_date in consecutive_dates
            )

            self._model.add(total_night_shifts <= constants.MAX_CONSECUTIVE_NIGHT_SHIFTS)

    def create_soft_constraints(self) -> base.PenaltyExpression:
        penalty: base.PenaltyExpression = 0

        for worker, (day_1, day_2, day_3, day_4) in itertools.product(
            self._config.all_workers,
            more_itertools.sliding_window(self._config.period, 4),
        ):
            total_night_shifts = sum(
                self._shift_assignments.get(worker, types.Shift.NIGHT, day_1)
                for day in (day_1, day_2)
            )

            total_rests = sum(
                self._shift_assignments.get(worker, shift, day)
                for shift, day in itertools.product(
                    types.Shift.all_resting_shifts(), (day_3, day_4)
                )
            )

            has_two_night_shifts = self._model.new_bool_var("")
            self._model.add(total_night_shifts >= 2).only_enforce_if(has_two_night_shifts)

            has_two_rests = self._model.new_bool_var("")
            self._model.add(total_rests >= 2).only_enforce_if(has_two_rests)

            should_penalize = self._model.new_bool_var("")
            self._model.add_bool_and([has_two_night_shifts, ~has_two_rests]).only_enforce_if(
                should_penalize
            )

            penalty += should_penalize * self._penalty_per_unit

        return penalty

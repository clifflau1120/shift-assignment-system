"""Module of `MorningShiftConstraint`."""

import itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base, utils


class MorningShiftConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that represents:

    - Hard constraint: ensures a certain number of workers assigned every morning
    - Soft constraint: penalizes morning schedules with non-maximum number of workers
    """

    def add_hard_constraints(self) -> None:
        for scheduled_date in self._config.period:
            total_workers_in_the_morning = sum(
                self._shift_assignments.get(worker, shift, scheduled_date)
                for worker, shift in itertools.product(
                    self._config.all_workers,
                    types.Shift.all_morning_shifts(),
                )
            )

            self._model.add(total_workers_in_the_morning >= constants.MIN_WORKERS_IN_THE_MORNING)
            self._model.add(total_workers_in_the_morning <= constants.MAX_WORKERS_IN_THE_MORNING)

    def create_soft_constraints(self) -> base.PenaltyExpression:
        penalty: base.PenaltyExpression = 0

        for scheduled_date in self._config.period:
            shift_assignments_in_the_morning = [
                self._shift_assignments.get(worker, shift, scheduled_date)
                for worker, shift in itertools.product(
                    self._config.all_workers,
                    types.Shift.all_morning_shifts(),
                )
            ]

            penalty += utils.create_soft_constraint(  # pyright: ignore
                model=self._model,
                events=shift_assignments_in_the_morning,
                soft_min=constants.MAX_WORKERS_IN_THE_MORNING,
                penalty_per_unit=self._penalty_per_unit,
            )

        return penalty

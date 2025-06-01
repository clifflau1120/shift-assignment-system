"""Module of `AfternoonShiftConstraint`."""

import itertools

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base, utils


class AfternoonShiftConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that represents:

    - Hard constraint: ensures a certain number of workers assigned every afternoon
    - Soft constraint: penalizes afternoon schedules with non-maximum number of workers
    """

    def add_hard_constraints(self) -> None:
        min_workers = constants.MIN_WORKERS_IN_THE_AFTERNOON
        max_workers = constants.MAX_WORKERS_IN_THE_AFTERNOON

        for scheduled_date in self._config.period:
            total_workers_in_the_afternoon = sum(
                self._shift_assignments.get(worker, shift, scheduled_date)
                for worker, shift in itertools.product(
                    self._config.all_workers,
                    types.Shift.all_afternoon_shifts(),
                )
            )

            self._model.add(total_workers_in_the_afternoon >= min_workers)
            self._model.add(total_workers_in_the_afternoon <= max_workers)

    def create_soft_constraints(self) -> base.PenaltyExpression:
        penalty: base.PenaltyExpression = 0

        for scheduled_date in self._config.period:
            shift_assignments_in_the_afternoon = [
                self._shift_assignments.get(worker, shift, scheduled_date)
                for worker, shift in itertools.product(
                    self._config.all_workers,
                    types.Shift.all_afternoon_shifts(),
                )
            ]

            penalty += utils.create_soft_constraint(  # pyright: ignore
                model=self._model,
                events=shift_assignments_in_the_afternoon,
                soft_min=constants.MAX_WORKERS_IN_THE_AFTERNOON,
                penalty_per_unit=self._penalty_per_unit,
            )

        return penalty

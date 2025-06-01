"""Module of `WorkingHoursConstraint`."""

import itertools
import typing
from datetime import date

from shift_scheduler.schedules import constants, types
from shift_scheduler.schedules.constraints import base
from shift_scheduler.utils import datetime_utils


class WorkingHoursConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures every worker has a fixed number of working hours.
    """

    def add_hard_constraints(self) -> None:
        for worker in self._config.full_time_workers:
            working_hours = sum(
                self._shift_assignments.get(worker, shift, scheduled_date)
                * constants.WORKING_HOURS[shift]
                for shift, scheduled_date in itertools.product(types.Shift, self._config.period)
            )

            annual_leaves = self._config.workers[worker].requests.get(types.Shift.ANNUAL_LEAVE, [])
            working_hours += self._get_working_hour_adjustment(annual_leaves)

            self._model.add(working_hours == constants.TOTAL_WORKING_HOURS)

    @staticmethod
    def _get_working_hour_adjustment(annual_leaves: typing.Iterable[date]) -> int:
        """Calculate the working hour adjustment for consecutive annual leaves."""

        annual_leaves = list(sorted(annual_leaves))
        seven_consecutive_annual_leaves = datetime_utils.count_n_date_sequences(7, annual_leaves)

        working_hours = (
            seven_consecutive_annual_leaves
            * constants.WORKING_HOURS_FOR_SEVEN_CONSECUTIVE_ANNUAL_LEAVES
        )

        unadjusted_working_hours = (
            7 * seven_consecutive_annual_leaves * constants.WORKING_HOURS[types.Shift.ANNUAL_LEAVE]
        )

        return working_hours - unadjusted_working_hours

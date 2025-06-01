"""Module of `PublicHolidaysConstraint`."""

import holidays

from shift_scheduler.schedules import types
from shift_scheduler.schedules.constraints import base


class PublicHolidaysConstraint(base.ShiftAssignmentConstraint):
    """
    A `ShiftAssignmentConstraint` that ensures public holidays or compensation leaves are taken,
    including carryovers from the previous schedule or to the next schedule.
    """

    def add_hard_constraints(self) -> None:
        public_holidays = holidays.country_holidays("HK")
        total_public_holidays = sum(date_ in public_holidays for date_ in self._config.period)

        for worker in self._config.full_time_workers:
            preference = self._config.workers[worker]

            public_holidays_taken = sum(
                self._shift_assignments.get(worker, types.Shift.PUBLIC_HOLIDAY, scheduled_date)
                for scheduled_date in self._config.period
            )

            self._model.add(
                public_holidays_taken == (total_public_holidays + preference.carryovers)
            )

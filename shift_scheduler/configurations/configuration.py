"""Module of configurations."""

import functools
from datetime import date

from pydantic import BaseModel, model_validator, Field

from shift_scheduler.configurations.io import IoConfiguration
from shift_scheduler.configurations.worker import WorkerPreferences
from shift_scheduler.schedules import types, constants
from shift_scheduler.utils import datetime_utils


class Configuration(BaseModel, frozen=True):
    """Configures the constraints of the shift schedule."""

    start_date: date
    """The start date of the shift schedule."""

    end_date: date
    """The end date of the shift schedule."""

    total_working_hours: int = Field(ge=min(constants.WORKING_HOURS.values()))
    """The total working hours required for every full-time worker."""

    io: IoConfiguration
    """Configures the I/O of the application."""

    workers: dict[types.WorkerName, WorkerPreferences]
    """Preferences of each worker in the shift schedule."""

    @functools.cached_property
    def period(self) -> list[date]:
        """The period of the shift schedule."""

        return list(datetime_utils.date_range(self.start_date, self.end_date))

    @functools.cached_property
    def full_time_workers(self) -> list[types.WorkerName]:
        """A list of full-time workers."""

        return [name for name, worker in self.workers.items() if worker.is_full_time]

    @functools.cached_property
    def part_time_workers(self) -> list[types.WorkerName]:
        """A list of part-time workers."""

        return [name for name, worker in self.workers.items() if not worker.is_full_time]

    @functools.cached_property
    def all_workers(self) -> list[types.WorkerName]:
        """A list of all workers."""

        return list(self.workers.keys())

    @model_validator(mode="after")
    def _ensure_start_date_is_before_end_date(self):
        if self.start_date < self.end_date:
            return self

        raise ValueError("start_date must be before end_date.")

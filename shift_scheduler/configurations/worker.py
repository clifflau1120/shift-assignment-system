"""Module of `WorkerConfiguration`."""

import itertools
from datetime import date

from pydantic import BaseModel, Field, field_validator

from shift_scheduler.schedules import types


class WorkerPreferences(BaseModel):
    """Configuration of a worker."""

    is_full_time: bool
    """Whether this worker is a full-time healthcare assistant."""

    accept_pa_shifts: bool = False
    """
    Whether this worker accepts a morning shift after an afternoon shift.

    Even this flag is set, such a shift arrangement is still depriortized.
    """

    carryovers: int = 0
    """
    The number of public holiday carryovers
    from the previous schedule or to the next schedule.
    """

    requests: dict[types.Shift, set[date]] = Field(default_factory=dict)
    """The requested shifts of the worker."""

    @field_validator("requests", mode="after")
    @classmethod
    def _ensure_at_most_one_birthday_leave(
        cls, requests: dict[types.Shift, set[date]]
    ) -> dict[types.Shift, set[date]]:
        """Ensures that birthday leave cannot be set to multiple dates."""

        birthday_leaves = requests.get(types.Shift.BIRTHDAY_LEAVE) or set()

        if len(birthday_leaves) > 1:
            raise ValueError("Birthday leave cannot be set to multiple dates.")

        return requests

    @field_validator("requests", mode="after")
    @classmethod
    def _ensure_no_contradicted_requests(
        cls, requests: dict[types.Shift, set[date]]
    ) -> dict[types.Shift, set[date]]:
        """Ensures that birthday leave cannot be set to multiple dates."""

        for (shift_a, dates_a), (shift_b, dates_b) in itertools.combinations(requests.items(), 2):
            if contradictions := dates_a & dates_b:
                contradictions_str = str.join(
                    ",", (requested_date.isoformat() for requested_date in contradictions)
                )

                raise ValueError(
                    f"Must not request the same date(s) for {shift_a} and {shift_b}: "
                    + contradictions_str
                )

        return requests

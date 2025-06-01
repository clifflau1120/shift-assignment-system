"""Module that serializes shift assignments."""

import itertools
import typing

from ortools.sat.python import cp_model

from shift_scheduler import configurations
from shift_scheduler.schedules import types, variables

TAG_REQUEST = "R"
TAG_FULL_TIME = "SA"
TAG_PART_TIME = "替假SA"

FULL_DATE_FORMAT = "%m/%d/%Y"
WEEKDAY_TRANSLATIONS = ["一", "二", "三", "四", "五", "六", "日"]


def serialize_solution(
    solver: cp_model.CpSolver,
    config: configurations.Configuration,
    shift_assignments: variables.ShiftAssignmentVariables,
) -> typing.Generator[list[str], None, None]:
    """Serialize the solution of the shift schedule to CSV rows."""

    serialized_dates = [str(scheduled_date.day) for scheduled_date in config.period]
    serialized_weekdays = [
        WEEKDAY_TRANSLATIONS[scheduled_date.weekday()] for scheduled_date in config.period
    ]

    yield [config.period[0].strftime(FULL_DATE_FORMAT), *serialized_dates]
    yield [config.period[-1].strftime(FULL_DATE_FORMAT), *serialized_weekdays]

    for worker, worker_tag in itertools.chain(
        itertools.product(config.full_time_workers, [TAG_FULL_TIME]),
        itertools.product(config.part_time_workers, [TAG_PART_TIME]),
    ):
        tags: list[str] = [worker_tag]
        shifts: list[str] = [worker]

        preference = config.workers[worker]
        requested_dates = set(itertools.chain.from_iterable(preference.requests.values()))

        for scheduled_date in config.period:
            for shift in types.Shift:
                shift_assignment = shift_assignments.get(worker, shift, scheduled_date)

                if solver.boolean_value(shift_assignment):
                    if scheduled_date in requested_dates:
                        tags.append(TAG_REQUEST)
                    else:
                        tags.append("")

                    shifts.append(shift.value)
                    break
            else:
                shifts.append("")
                tags.append("")

        yield tags
        yield shifts

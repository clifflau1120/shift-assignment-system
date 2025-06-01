"""Module of scheduling constants."""

from shift_scheduler.schedules import types

MAX_CONSECUTIVE_WORKING_DAYS = 6
"""The maximum number of consecutive working days that can be assigned to a worker."""

MAX_CONSECUTIVE_AP_SHIFTS = 5
"""The maximum number of consecutive A/P shifts that can be assigned to a worker."""

MAX_CONSECUTIVE_NIGHT_SHIFTS = 2
"""The maximum number of consecutive night shifts that can be assigned to a worker."""

MAX_CONSECUTIVE_TIME_OFFS = 2
"""The maximum number of consecutive time-offs that can be assigned to a worker."""

MIN_WORKERS_IN_THE_MORNING = 3
"""The minimum number of workers in the morning."""

MAX_WORKERS_IN_THE_MORNING = 4
"""The maximum number of workers in the morning."""

MIN_WORKERS_IN_THE_AFTERNOON = 3
"""The minimum number of workers in the afternoon."""

MAX_WORKERS_IN_THE_AFTERNOON = 4
"""The maximum number of workers in the afternoon."""

NUM_WORKERS_AT_NIGHT = 2
"""The number of workers at night."""

MIN_TIME_OFFS = 9
"""The minimum days of time-offs in a schedule."""

MAX_TIME_OFFS = 10
"""The maximum days of time-offs in a schedule."""

WORKING_HOURS = {
    types.Shift.MORNING: 8,
    types.Shift.MORNING_SHORTENED: 7,
    types.Shift.MORNING_EXTENDED: 9,
    types.Shift.AFTERNOON: 8,
    types.Shift.AFTERNOON_SHORTENED: 7,
    types.Shift.AFTERNOON_EXTENDED: 9,
    types.Shift.NIGHT: 9,
    types.Shift.TIME_OFF: 0,
    types.Shift.ANNUAL_LEAVE: 8,
    types.Shift.BIRTHDAY_LEAVE: 8,
    types.Shift.PUBLIC_HOLIDAY: 8,
}
"""A map of shift types to working hours."""

WORKING_HOURS_FOR_SEVEN_CONSECUTIVE_ANNUAL_LEAVES = 44
"""A special number of working hours equivalent to every 7 consecutive annual leaves."""

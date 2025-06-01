"""Module of shift assignment constraints."""

from .after_afternoon_shifts import AfterAfternoonShiftsConstraint
from .after_night_shifts import AfterNightShiftsConstraint
from .annual_leaves import AnnualLeavesConstraint
from .birthday_leave import BirthdayLeaveConstraint
from .consecutive_ap_shifts import ConsecutiveApShiftsConstraint
from .consecutive_night_shifts import ConsecutiveNightShiftsConstraint
from .consecutive_time_offs import ConsecutiveTimeOffsConstraint
from .consecutive_working_days import ConsecutiveWorkingDaysConstraint
from .daily_assignment import DailyAssignmentConstraint
from .part_time import PartTimeAssignmentConstraint
from .public_holidays import PublicHolidaysConstraint
from .requested_shifts import RequestedShiftsConstraint
from .time_offs import TimeOffConstraint
from .workers_in_afternoon_shifts import AfternoonShiftConstraint
from .workers_in_morning_shifts import MorningShiftConstraint
from .workers_in_night_shifts import NightShiftConstraint
from .workers_in_special_working_shifts import SpecialWorkingShiftConstraint
from .working_hours import WorkingHoursConstraint

__all__ = [
    "AfterAfternoonShiftsConstraint",
    "AfterNightShiftsConstraint",
    "AnnualLeavesConstraint",
    "BirthdayLeaveConstraint",
    "ConsecutiveApShiftsConstraint",
    "ConsecutiveNightShiftsConstraint",
    "ConsecutiveTimeOffsConstraint",
    "ConsecutiveWorkingDaysConstraint",
    "DailyAssignmentConstraint",
    "PartTimeAssignmentConstraint",
    "PublicHolidaysConstraint",
    "RequestedShiftsConstraint",
    "TimeOffConstraint",
    "AfternoonShiftConstraint",
    "MorningShiftConstraint",
    "NightShiftConstraint",
    "SpecialWorkingShiftConstraint",
    "WorkingHoursConstraint",
]

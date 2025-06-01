"""Module of static types."""

import enum
import typing
from datetime import date

WorkerName = str


class Shift(str, enum.Enum):
    """An enumeration of work timeslots per day."""

    MORNING = "A"
    """A morning shift from 7:00 to 15:00."""

    MORNING_SHORTENED = "7-2"
    """A shortened morning shift from 7:00 to 14:00."""

    MORNING_EXTENDED = "7-4"
    """An extended morning shift from 7:00 to 16:00."""

    AFTERNOON = "P"
    """An afternoon shift from 14:00 to 22:00."""

    AFTERNOON_SHORTENED = "2-9"
    """A shortened afternoon shift from 14:00 to 21:00."""

    AFTERNOON_EXTENDED = "1-10"
    """An extended shift from 13:00 to 22:00."""

    NIGHT = "N"
    """A night shift from 22:00 to 07:00."""

    TIME_OFF = "_"
    """A regular time-off."""

    ANNUAL_LEAVE = "AL"
    """An annual leave."""

    BIRTHDAY_LEAVE = "BL"
    """A birthday leave."""

    PUBLIC_HOLIDAY = "PH"
    """
    A public holiday, a compensation leave
    or a carryover of the above from the previous schedule.
    """

    @classmethod
    def all_morning_shifts(cls) -> set["Shift"]:
        """A set of all types of morning shifts."""

        return {cls.MORNING, cls.MORNING_SHORTENED, cls.MORNING_EXTENDED}

    @classmethod
    def all_afternoon_shifts(cls) -> set["Shift"]:
        """A set of all types of afternoon shifts."""

        return {cls.AFTERNOON, cls.AFTERNOON_SHORTENED, cls.AFTERNOON_EXTENDED}

    @classmethod
    def regular_working_shifts(cls) -> set["Shift"]:
        """A set of all regular working shifts."""

        return {cls.MORNING, cls.AFTERNOON, cls.NIGHT}

    @classmethod
    def special_working_shifts(cls) -> set["Shift"]:
        """A set of all shortened/extended shifts."""

        return {
            cls.MORNING_SHORTENED,
            cls.MORNING_EXTENDED,
            cls.AFTERNOON_SHORTENED,
            cls.AFTERNOON_EXTENDED,
        }

    @classmethod
    def all_working_shifts(cls) -> set["Shift"]:
        """A set of all working shifts."""

        return cls.regular_working_shifts() & cls.special_working_shifts()

    @classmethod
    def all_resting_shifts(cls) -> set["Shift"]:
        """A set of all types of resting shifts."""

        return set(cls) - cls.all_working_shifts()


class ShiftAssignment(typing.NamedTuple):
    """An assignment of a worker to a shift."""

    worker: WorkerName

    shift: Shift

    scheduled_date: date

    def __str__(self) -> str:
        return (
            f"{self.worker} is assigned to Shift {self.shift} at {self.scheduled_date.isoformat()}"
        )

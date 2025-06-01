import abc
import typing

from ortools.sat.python import cp_model

from shift_scheduler import configurations
from shift_scheduler.schedules import variables

NO_PENALTY = 0

PenaltyExpression = cp_model.ObjLinearExprT
"""A linear expression that represents the penalty incurred for soft constraint violation."""


class ShiftAssignmentConstraint(abc.ABC):
    """A constraint to shift assignment."""

    @typing.final
    def __init__(
        self,
        model: cp_model.CpModel,
        config: configurations.Configuration,
        shift_assignments: variables.ShiftAssignmentVariables,
        *,
        penalty_per_unit: int = 1,
    ):
        self._model = model
        self._config = config
        self._shift_assignments = shift_assignments

        self._penalty_per_unit = penalty_per_unit

    def add_hard_constraints(self) -> None:
        """Add hard constraints to shift assignments."""

    def create_soft_constraints(self) -> PenaltyExpression:
        """Create a penalty expression that represents the soft constraints."""

        return NO_PENALTY

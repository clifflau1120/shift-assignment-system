"""Module of `ShiftManager`."""

import typing

import typing_extensions
from ortools.sat import cp_model_pb2
from ortools.sat.python import cp_model

from shift_scheduler import configurations
from shift_scheduler.schedules import exceptions, variables
from shift_scheduler.schedules.constraints import base as base_constraint


@typing.final
class ShiftManager:
    """A shift scheduler that manages the constraint programming model."""

    def __init__(
        self,
        config: configurations.Configuration,
        model: cp_model.CpModel | None = None,
        solver: cp_model.CpSolver | None = None,
        shift_assignments: variables.ShiftAssignmentVariables | None = None,
    ):
        self._config = config

        self._model = model or cp_model.CpModel()
        self._solver = solver or cp_model.CpSolver()
        self._constraints: list[base_constraint.ShiftAssignmentConstraint] = []

        self._shift_assignments = variables.ShiftAssignmentVariables.from_config(
            self._model,
            self._config,
        )

        self._set_solver_parameters()

    @property
    def config(self) -> configurations.Configuration:
        """The configuration of the schedule."""

        return self._config

    @property
    def model(self) -> cp_model.CpModel:
        """The constraint programming model."""

        return self._model

    @property
    def solver(self) -> cp_model.CpSolver:
        """The constraint programming solver."""

        return self._solver

    @property
    def shift_assignments(self) -> variables.ShiftAssignmentVariables:
        """The shift assignment variables."""

        return self._shift_assignments

    def add_constraint_module(
        self,
        constraint_cls: type[base_constraint.ShiftAssignmentConstraint],
        *,
        penalty_per_unit: int = 1,
    ) -> typing_extensions.Self:
        """Add a shift assignment constraint to the scheduler."""

        constraint = constraint_cls(
            self.model,
            self.config,
            self.shift_assignments,
            penalty_per_unit=penalty_per_unit,
        )
        self._constraints.append(constraint)

        return self

    def solve(self) -> cp_model_pb2.CpSolverStatus:
        """Solve the scheduling problem."""

        penalties = base_constraint.PenaltyExpression = 0.0

        for constraint in self._constraints:
            constraint.add_hard_constraints()
            penalties += constraint.create_soft_constraints()  # pyright: ignore

        self._model.minimize(penalties)  # pyright: ignore
        return self._solver.solve(self._model)

    def _set_solver_parameters(self):
        """Use the configuration object to set solver parameters."""

        for key, value in self._config.sat_parameters.items():
            try:
                setattr(self._solver.parameters, key, value)
            except AttributeError as cause:
                raise exceptions.SatParameterError(key) from cause

"""Module of `ShiftAssignmentVariables`."""

import functools
import itertools
from datetime import date

from ortools.sat.python import cp_model

from shift_scheduler import configurations
from shift_scheduler.schedules import types


class ShiftAssignmentVariables:
    """A registry of variables, each of which represents a particular shift assignment."""

    def __init__(self, model: cp_model.CpModel):
        self._model = model
        self._variables: dict[types.ShiftAssignment, cp_model.IntVar] = {}

    @classmethod
    def from_config(
        cls,
        model: cp_model.CpModel,
        config: configurations.Configuration,
    ) -> "ShiftAssignmentVariables":
        """Create variables from the model configuration."""

        variables = cls(model)

        shift_assignments = itertools.starmap(
            types.ShiftAssignment,
            itertools.product(config.all_workers, types.Shift, config.period),
        )

        for shift_assignment in shift_assignments:
            _ = variables.add(shift_assignment)

        return variables

    @functools.singledispatchmethod
    def add(self, *args) -> cp_model.IntVar:
        """Add a new boolean variable to represent the given shift assignment."""

        raise NotImplementedError  # pragma: no cover

    @add.register
    def _(self, worker: str, shift: types.Shift, scheduled_date: date) -> cp_model.IntVar:
        shift_assignment = types.ShiftAssignment(worker, shift, scheduled_date)
        self._variables[shift_assignment] = self._model.new_bool_var(str(shift_assignment))

        return self._variables[shift_assignment]

    @add.register
    def _(self, shift_assignment: types.ShiftAssignment) -> cp_model.IntVar:
        self._variables[shift_assignment] = self._model.new_bool_var(str(shift_assignment))
        return self._variables[shift_assignment]

    def __setitem__(self, shift_assignment: types.ShiftAssignment):
        self.add(shift_assignment)

    @functools.singledispatchmethod
    def get(self, *args) -> cp_model.IntVar:
        """Get the variable of a particular shift assignment."""

        raise NotImplementedError  # pragma: no cover

    @get.register
    def _(self, worker: str, shift: types.Shift, scheduled_date: date) -> cp_model.IntVar:
        shift_assignment = types.ShiftAssignment(worker, shift, scheduled_date)
        return self._variables[shift_assignment]

    @get.register
    def _(self, shift_assignment: types.ShiftAssignment) -> cp_model.IntVar:
        return self._variables[shift_assignment]

    def __getitem__(self, shift_assignment: types.ShiftAssignment) -> cp_model.IntVar:
        return self.get(shift_assignment)

    def __contains__(self, shift_assignment: types.ShiftAssignment) -> bool:
        return shift_assignment in self._variables

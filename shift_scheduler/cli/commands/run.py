"""Module of the `run` command."""

import logging
import pathlib

import typer
import typing_extensions
from ortools.sat import cp_model_pb2

from shift_scheduler import configurations
from shift_scheduler.schedules import constraints, manager
from shift_scheduler.utils import file_utils, serialization_utils

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def run(
    ctx: typer.Context,
    config_file_path: typing_extensions.Annotated[
        pathlib.Path,
        typer.Option(
            "--config",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The path to the configuration file.",
        ),
    ],
):
    """Generate a shift schedule with respect to the configured constraints."""

    config = configurations.Configuration.model_validate_json(config_file_path.read_bytes())
    logger.info("Loaded configurations: %s", config_file_path)

    shift_manager = manager.ShiftManager(config)

    (
        shift_manager.add_constraint_module(constraints.DailyAssignmentConstraint)
        .add_constraint_module(constraints.PartTimeAssignmentConstraint, penalty_per_unit=1)  # 7
        .add_constraint_module(constraints.AfternoonShiftConstraint, penalty_per_unit=5)  # 0
        .add_constraint_module(constraints.MorningShiftConstraint, penalty_per_unit=5)  # 0
        .add_constraint_module(constraints.NightShiftConstraint)
        .add_constraint_module(constraints.TimeOffConstraint)
        .add_constraint_module(constraints.AnnualLeavesConstraint)
        .add_constraint_module(constraints.BirthdayLeaveConstraint)
        .add_constraint_module(constraints.PublicHolidaysConstraint)
        .add_constraint_module(constraints.RequestedShiftsConstraint)
        .add_constraint_module(constraints.SpecialWorkingShiftConstraint, penalty_per_unit=2)  # 8
        .add_constraint_module(constraints.WorkingHoursConstraint)
        .add_constraint_module(constraints.ConsecutiveWorkingDaysConstraint)
        .add_constraint_module(constraints.ConsecutiveApShiftsConstraint)
        .add_constraint_module(constraints.ConsecutiveNightShiftsConstraint, penalty_per_unit=4)
        .add_constraint_module(constraints.ConsecutiveTimeOffsConstraint)
        .add_constraint_module(constraints.AfterAfternoonShiftsConstraint, penalty_per_unit=3)  # 9
        .add_constraint_module(constraints.AfterNightShiftsConstraint)
    )

    logger.info("Started to solve for the optimal schedule.")

    # Solve the model
    match shift_manager.solve():
        case cp_model_pb2.OPTIMAL | cp_model_pb2.FEASIBLE:
            logger.info("Found a schedule that meets all the constraints.")

            file_path = file_utils.prepare_file_path(shift_manager.config)

            rows = serialization_utils.serialize_solution(
                shift_manager.solver,
                shift_manager.config,
                shift_manager.shift_assignments,
            )

            file_utils.write_solution(rows, file_path)

            logger.debug("Objective value: %f", shift_manager.solver.objective_value)
            logger.info("Wrote the schedule to: %s", file_path)
        case cp_model_pb2.INFEASIBLE:
            logger.info("Failed to find a schedule that meets all the constraints.")
        case cp_model_pb2.MODEL_INVALID:
            logger.critical("Failed to set up the constraint programming model.")
        case cp_model_pb2.UNKNOWN:
            logger.warning("Failed to find a schedule within maximum search depth.")

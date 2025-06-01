"""Module of the CLI application."""

import typer

from shift_scheduler.cli.commands.config_schema import app as config_schema_command
from shift_scheduler.cli.commands.run import app as run_command
from shift_scheduler.cli.commands.version import app as version_command

app = typer.Typer()
app.add_typer(config_schema_command)
app.add_typer(run_command)
app.add_typer(version_command)

if __name__ == "__main__":
    app()

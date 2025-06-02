"""Module of the CLI application."""

import logging

import rich.logging
import typer
import typing_extensions

from shift_scheduler.cli.commands.config_schema import app as config_schema_command
from shift_scheduler.cli.commands.run import app as run_command
from shift_scheduler.cli.commands.version import app as version_command

app = typer.Typer()
app.add_typer(config_schema_command)
app.add_typer(run_command)
app.add_typer(version_command)


@app.callback()
def callback(
    debug: typing_extensions.Annotated[bool, typer.Option()] = False,
):
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
    )


if __name__ == "__main__":
    app()

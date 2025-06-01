"""Module of the `version` command."""

import typer

from shift_scheduler.version import __version__

app = typer.Typer()


@app.command(help="Display the version of shift-scheduler.")
def version():
    print(__version__)

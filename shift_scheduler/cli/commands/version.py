"""Module of the `version` command."""

import typer

from shift_scheduler.version import __version__

app = typer.Typer()


@app.command()
def version():
    """Show the version of shift-scheduler."""

    print(__version__)

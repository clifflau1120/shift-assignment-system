"""Module of the `config_schema` command."""

import json
import sys

import typer

from shift_scheduler import configurations

app = typer.Typer()


@app.command()
def config_schema():
    """Print the JSON schema of the configuration to console."""

    json_schema = configurations.Configuration.model_json_schema()
    sys.stdout.write(json.dumps(json_schema, indent=2))

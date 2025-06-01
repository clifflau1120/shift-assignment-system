"""Module of `IoConfiguration`."""

import pathlib

from pydantic import BaseModel


class IoConfiguration(BaseModel):
    """Configures the I/O behavior of the application."""

    encoding: str = "utf-8"
    """The character encoding scheme to write the CSV file."""

    output_file_name: str
    """
    The format of the output file name with `datetime.strftime` format codes.

    See also: https://docs.python.org/3/library/datetime.html#format-codes
    """

    output_directory: pathlib.Path = pathlib.Path("outputs")
    """The directory to write the output file to."""

"""Module that interacts with the file system."""

import csv
import pathlib
import typing

from shift_scheduler import configurations


def prepare_file_path(config: configurations.Configuration) -> pathlib.Path:
    """Prepare the output file path."""

    config.io.output_directory.mkdir(parents=True, exist_ok=True)
    return config.io.output_directory / config.start_date.strftime(config.io.output_file_name)


def write_solution(rows: typing.Iterable[list[str]], file_path: pathlib.Path):
    """Write the CSV rows to `file_path`."""

    with open(file_path, "w", encoding="utf-8") as fin:
        writer = csv.writer(fin, dialect="excel")
        writer.writerows(rows)

"""Module of exceptions."""


class SatParameterError(Exception):
    """An exception raised when a sat parameter does not exist."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return (
            f'The SAT parameter "{self.name}" does not exist; '
            "please remove this option from your configuration file."
        )

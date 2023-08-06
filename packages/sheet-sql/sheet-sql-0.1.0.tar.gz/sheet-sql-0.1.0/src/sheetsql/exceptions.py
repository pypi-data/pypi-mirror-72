"""Custom exceptions."""


class InvalidQueryException(Exception):
    """Raises if the table query (tq) is invalid."""

    pass


class InvalidRowTypeException(Exception):
    """Raises if the row type is invalid."""

    pass


class SpreadsheetNotFoundException(Exception):
    """Raises if a spreadsheet is not found."""

    pass

"""Boardfarm DOCSIS exceptions."""

from boardfarm.exceptions import BoardfarmException


class ConfigEncodingError(BoardfarmException):
    """Raise this on docsis config encoding error."""

"""Boardfarm DOCSIS exceptions."""

from boardfarm3.exceptions import BoardfarmException


class ConfigEncodingError(BoardfarmException):
    """Raise this on docsis config encoding error."""

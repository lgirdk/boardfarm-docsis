"""Boardfarm DOCSIS exceptions."""

from boardfarm3.exceptions import BoardfarmException


class ConfigEncodingError(BoardfarmException):
    """Raise this on docsis config encoding error."""

    def __init__(self, filename: str):  # noqa: D107
        super().__init__(f"Failed to encode modem config {filename}")

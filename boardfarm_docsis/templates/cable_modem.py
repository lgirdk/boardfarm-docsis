"""Boardfarm DOCSIS cable modem device template."""

from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods


class CableModem(ABC):
    """Boardfarm DOCSIS cable modem device template."""

    @property
    @abstractmethod
    def gui_password(self) -> str:
        """Password to GUI."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_gateway(self) -> str:
        """Lan gateway IP."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_private_gateway(self) -> str:
        """Lan private gateway IP (modem mode)."""
        raise NotImplementedError

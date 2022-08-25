"""Boardfarm DOCSIS cable modem device template."""

from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods


class CableModem(ABC):
    """Boardfarm DOCSIS cable modem device template."""

    @abstractmethod
    @property
    def tr69_cpe_id(self) -> str:
        """TR-69 CPE Identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_provision_mode(self) -> str:
        """Get cable modem provision mode from boot file.

        :returns: cable modem provision mode
        :raises EnvConfigError: when failed to find provision mode
        """
        raise NotImplementedError

"""Cable modem template."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from boardfarm3.templates.cpe.cpe import CPE
from debtcollector import moves

if TYPE_CHECKING:
    from boardfarm3_docsis.templates.cable_modem.cable_modem_hw import CableModemHW
    from boardfarm3_docsis.templates.cable_modem.cable_modem_sw import CableModemSW


class CableModem(CPE):
    """CPE Template."""

    @property
    @abstractmethod
    def hw(self) -> CableModemHW:  # pylint: disable=invalid-name
        """CPE Software."""
        raise NotImplementedError

    @property
    @abstractmethod
    def sw(self) -> CableModemSW:  # pylint: disable=invalid-name
        """CPE Software."""
        raise NotImplementedError

    @property
    @moves.moved_property("hw.mac_address")
    def cm_mac(self) -> str:
        """MAC Address.

        :return: the CM mac address (usually the wan0 mac address)
        :rtype: str
        """
        return self.hw.mac_address

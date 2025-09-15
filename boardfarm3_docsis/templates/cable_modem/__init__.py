"""Boardfarm LGI shared cable modem templates."""

from boardfarm3_docsis.templates.cable_modem.cable_modem import CableModem
from boardfarm3_docsis.templates.cable_modem.cable_modem_hw import CableModemHW
from boardfarm3_docsis.templates.cable_modem.cable_modem_mibs import CableModemMibs
from boardfarm3_docsis.templates.cable_modem.cable_modem_sw import CableModemSW

__all__ = ["CableModem", "CableModemHW", "CableModemMibs", "CableModemSW"]

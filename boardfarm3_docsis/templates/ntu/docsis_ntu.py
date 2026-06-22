"""DOCSIS NTU template."""

from __future__ import annotations

from abc import abstractmethod

from boardfarm3.templates.ntu.ntu import NTU


class DocsisNTU(NTU):
    """DOCSIS NTU Template.

    This will be defined in the future when we have a better
    understanding of the commonalities between the various NTUs
    used in the DOCSIS tests.
    """

    @property
    @abstractmethod
    def cm_mac(self) -> str:
        """MAC Address.

        :return: the CM mac address (usually the wan0 mac address)
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def is_online(self) -> bool:
        """Is cable modem online.

        :return: True if cable modem is in OPERATIONAL state, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def finalize_boot(self) -> bool:
        """Check if board SKU is the same as env & apply correct SKU if it is not set.

        .. note::
            * See OFW-1935 for details. Steps below
            * Send dmcli GET Device.X_LGI-COM_General.CustomerId
            * If it is the same as requested in env.json -> return True
            * echo {SKU_index} > /nvram/bootconfig_custindex
            * sync DUT FS
            * Reboot DUT

        :return: True if SKU already set correctly, False if we set it & reboot board
        :rtype: bool
        """
        raise NotImplementedError

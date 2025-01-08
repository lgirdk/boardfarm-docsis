"""DOCSIS Config file encoder module."""

import logging
import tempfile
from pathlib import Path

import pexpect
from boardfarm3.lib.connections.local_cmd import LocalCmd

from boardfarm3_docsis.exceptions import ConfigEncodingError

_LOGGER = logging.getLogger(__name__)


class DocsisConfigEncoder:
    """DOCSIS config file encoder.

    Requires the docsis compiler to be installed locally.
    """

    def __init__(self) -> None:
        """Initialize docsis config encoder."""
        self._encoder_cmd = "docsis"
        self._cfg_dict = {
            "cm": {
                "encoded_ext": ".cfg",
                "option": "-e",
                "key_file": "/dev/null",  # To be considered: parameterise
            },
            "mta": {
                "encoded_ext": ".bin",
                "option": "-eu -p",
                "key_file": "",  # To be considered: parameterise
            },
        }

    def _encode_config(self, config: str, mibs_path: list[str], is_mta: bool) -> Path:
        mibs_argument = ":".join(mibs_path)
        prefix = "mta" if is_mta else "cm"
        with tempfile.NamedTemporaryFile(
            mode="w",
            prefix=f"{prefix}-config-",
            suffix=".txt",
            encoding="utf-8",
        ) as named_temp_file:
            named_temp_file.write(config)
            named_temp_file.flush()
            cfg_file_path = Path(
                named_temp_file.name.replace(
                    ".txt",
                    self._cfg_dict[prefix]["encoded_ext"],
                ),
            )
            command = (
                f"{self._encoder_cmd} -M {mibs_argument} "
                f"{self._cfg_dict[prefix]['option']} {named_temp_file.name} "
                f"{self._cfg_dict[prefix]['key_file']} {cfg_file_path}"
            )
            _LOGGER.debug("Encoding modem config: %s", command)
            session = LocalCmd(
                "docsis-encoder",
                command,
                save_console_logs="",
                args=[],
            )
            session.expect(pexpect.EOF)
            if session.wait() != 0:
                raise ConfigEncodingError(named_temp_file.name)
        return cfg_file_path

    def encode_cm_config(self, cm_config: str, mibs_path: list[str]) -> Path:
        """Encode a given cable modem config text file(boot file).

        Override this method for bespoke compilations (e.g, different encriptions)

        :param cm_config: cable modem config text file path
        :type cm_config: str
        :param mibs_path: mibs directory paths
        :type mibs_path: list[str]
        :raises: ConfigEncodingError when docsis encoding failed
        :return: path to the docsis encoded config file
        :rtype: Path
        """
        return self._encode_config(config=cm_config, mibs_path=mibs_path, is_mta=False)

    def encode_mta_config(self, mta_config: str, mibs_path: list[str]) -> Path:
        """Encode a given MTA config text file.

        Override this method for bespoke compilations (e.g, different encriptions)

        :param mta_config: MTA config text file path
        :type mta_config: str
        :param mibs_path: mibs directory paths
        :type mibs_path: list[str]
        :raises: ConfigEncodingError when docsis encoding failed
        :return: path to the docsis encoded MTA file
        :type: Path
        """
        return self._encode_config(config=mta_config, mibs_path=mibs_path, is_mta=True)

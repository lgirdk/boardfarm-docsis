"""DOCSIS Config file encoder module."""

import logging
import tempfile
from pathlib import Path
from typing import List

import pexpect
from boardfarm.lib.connections.local_cmd import LocalCmd

from boardfarm_docsis.exceptions import ConfigEncodingError

_LOGGER = logging.getLogger(__name__)


class DocsisConfigEncoder:
    """DOCSIS config file encoder."""

    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        """Initialize docsis config encoder."""
        self._encoder_cmd = "docsis"

    def encode_cm_config(self, cm_config: str, mibs_path: List[str]) -> Path:
        """Encode cable modem config text file(boot file).

        :param cm_config: cable modem config text file
        :param mibs_path: mibs directory paths
        :raises ConfigEncodingError: when docsis encoding failed
        :returns: path to docsis encoded config file
        """
        print(cm_config)
        mibs_argument = ":".join(mibs_path)
        with tempfile.NamedTemporaryFile(
            mode="w", prefix="cm-config-", suffix=".txt", encoding="utf-8"
        ) as named_temp_file:
            named_temp_file.write(cm_config)
            named_temp_file.flush()
            cfg_file_path = Path(named_temp_file.name.replace(".txt", ".cfg"))
            command = (
                f"{self._encoder_cmd} -M {mibs_argument} "
                f"-e {named_temp_file.name} /dev/null {cfg_file_path}"
            )
            _LOGGER.debug("Encoding cable modem config: %s", command)
            session = LocalCmd("docsis-encoder", command, [])
            session.expect(pexpect.EOF)
            if session.wait() != 0:
                raise ConfigEncodingError("Failed to encode cable modem config")
        return cfg_file_path

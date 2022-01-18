from dataclasses import dataclass
from typing import Dict, List

from boardfarm.exceptions import UseCaseFailure


@dataclass
class AddObjectResponse:
    response: List[Dict[str, str]]
    object_name: str

    @property
    def instance_number(self) -> int:
        return self._instance_number

    def __post_init__(self) -> None:
        if self.object_name in str(self.response):
            self._instance_number = int(
                self.response[0]["key"][len(self.object_name) :].split(".")[0]
            )
        else:
            raise UseCaseFailure(
                f"AddObject Response could not be parsed. Response: {self.response}"
            )

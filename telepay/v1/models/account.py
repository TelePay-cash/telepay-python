from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Account:
    merchant: dict

    def __post_init__(self):
        pass

    @classmethod
    def from_json(cls, json: Any) -> "Account":
        del json["version"]
        return parse_json(cls, **json)

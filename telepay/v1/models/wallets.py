from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Wallets:
    wallets: list

    def __post_init__(self):
        pass

    @classmethod
    def from_json(cls, json: Any) -> "Wallets":
        return parse_json(cls, **json)

from dataclasses import dataclass
from typing import Any, List

from ..utils import parse_json


@dataclass
class Wallet:
    asset: str
    blockchain: str
    network: str
    balance: float

    @classmethod
    def from_json(cls, json: Any) -> "Wallet":
        return parse_json(cls, **json)


@dataclass
class Wallets:
    wallets: List[Wallet]

    def __post_init__(self):
        pass

    @classmethod
    def from_json(cls, json: Any) -> "Wallets":
        return parse_json(cls, **json)

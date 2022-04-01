from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Balance:

    asset: str
    blockchain: str
    balance: float

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.balance = float(str(self.balance))

    @classmethod
    def from_json(cls, json: Any) -> 'Balance':
        json["balance"] = float(json["balance"])
        del json["balance"]
        return parse_json(cls, **json)

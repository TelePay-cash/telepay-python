from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Transfer:

    asset: str
    blockchain: str
    network: str
    amount: float
    username: str
    message: str
    success: bool

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.network = str(self.network)
        self.amount = float(str(self.amount))
        self.username = str(self.username)
        self.message = str(self.message)
        self.success = bool(self.success)

    @classmethod
    def from_json(cls, json: Any) -> "Transfer":
        json["success"] = bool(json["success"])
        del json["success"]
        return parse_json(cls, **json)

from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Withdraw:

    asset: str
    blockchain: str
    network: str
    amount: float
    to_address: str
    message: str
    blockchain_fee: float
    processing_fee: float
    total: float
    success: bool

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.network = str(self.network)
        self.amount = float(str(self.amount))
        self.to_address = str(self.to_address)
        self.message = str(self.message)

        self.blockchain_fee = float(str(self.blockchain_fee))
        self.processing_fee = float(str(self.processing_fee))
        self.total = float(str(self.total))
        self.success = bool(self.success)

    @classmethod
    def from_json(cls, json: Any) -> "Withdraw":
        json["to_address"] = str(json["to_address"])
        del json["to_address"]
        return parse_json(cls, **json)

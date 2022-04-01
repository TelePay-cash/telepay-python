from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Invoice:

    asset: str
    blockchain: str
    network: str
    amount: float
    description: str
    success_url: str
    cancel_url: str
    expires_at: int

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.network = str(self.network)
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.success_url = str(self.success_url)
        self.cancel_url = str(self.cancel_url)
        self.expires_at = int(str(self.expires_at))

    @classmethod
    def from_json(cls, json: Any) -> 'Invoice':
        json["success_url"] = json["success_url"]
        json["cancel_url"] = json["cancel_url"]
        json["expires_at"] = json["expires_at"]
        del json["success_url"]
        del json["cancel_url"]
        del json["expires_at"]
        return parse_json(cls, **json)

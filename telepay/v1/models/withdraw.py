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

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.network = str(self.network)
        self.amount = float(str(self.amount))
        self.to_address = str(self.to_address)
        self.message = str(self.message)

    @classmethod
    def from_json(cls, json: Any) -> 'Withdraw':
        json['to_address'] = json['to_address']
        del json['to_address']
        return parse_json(cls, **json)

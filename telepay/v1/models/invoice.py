from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Invoice:

    asset: str
    blockchain: str
    network: str
    amount: str
    description: str

    number: str
    status: str
    metadata: str
    hidden_message: str

    success_url: str
    cancel_url: str
    explorer_url: str
    checkout_url: str

    created_at: str
    updated_at: str
    expires_at: int

    def __post_init__(self):
        self.asset = str(self.asset)
        self.blockchain = str(self.blockchain)
        self.network = str(self.network)
        self.amount = str(self.amount)
        self.description = str(self.description)

        self.success_url = str(self.success_url)
        self.cancel_url = str(self.cancel_url)
        
        self.status = str(self.status)
        self.hidden_message = str(self.hidden_message)
        self.number = str(self.number)
        self.metadata = str(self.metadata)
        
        self.created_at = str(self.created_at)
        self.updated_at = str(self.updated_at)
        self.expires_at = int(str(self.expires_at))

    @classmethod
    def from_json(cls, json: Any) -> 'Invoice':
        json['description'] = str(json['description'])
        del json['description']
        return parse_json(cls, **json)

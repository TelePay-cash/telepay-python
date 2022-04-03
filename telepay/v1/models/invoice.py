from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils import parse_json

FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


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

    created_at: datetime
    updated_at: datetime
    expires_at: datetime

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
        self.created_at = datetime.strptime(self.created_at, FORMAT)
        self.expires_at = datetime.strptime(self.expires_at, FORMAT)

        if self.updated_at is not None:
            self.updated_at = datetime.strptime(self.updated_at, FORMAT)

    @classmethod
    def from_json(cls, json: Any) -> "Invoice":
        return parse_json(cls, **json)


@dataclass
class InvoiceList:

    invoices: list

    def __post_init__(self):
        self.invoices = [Invoice.from_json(invoice) for invoice in self.invoices]

    @classmethod
    def from_json(cls, json: Any) -> "InvoiceList":
        return parse_json(cls, **json)

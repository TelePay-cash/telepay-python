from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Assets:

    url: str
    asset: str
    networks: str
    blockchain: str

    def __post_init__(self):
        self.url = str(self.url)
        self.assets = str(self.assets)
        self.networks = str(self.networks)
        self.blockchain = str(self.blockchain)

    @classmethod
    def from_json(cls, json: Any) -> 'Assets':
        json["asset"] = str(json["asset"])
        del json["asset"]
        return parse_json(cls, **json)

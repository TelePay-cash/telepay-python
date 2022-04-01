from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Assets:

    assets: str
    blockchain: str

    def __post_init__(self):
        self.assets = str(self.assets)
        self.blockchain = str(self.blockchain)

    @classmethod
    def from_json(cls, json: Any) -> 'Assets':
        json["assets"] = json["assets"]
        del json["assets"]
        return parse_json(cls, **json)

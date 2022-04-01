from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Info:

    name: str
    url: str  # AnyUrl
    logo_url: str
    logo_thumbnail_url: str
    first_name: str
    last_name: str
    username: str

    def __post_init__(self):
        self.name = str(self.name)
        self.url = str(self.url)
        self.logo_url = str(self.logo_url)
        self.logo_thumbnail_url = str(self.logo_thumbnail_url)
        self.first_name = str(self.first_name)
        self.last_name = str(self.last_name)
        self.username = str(self.username)

    @classmethod
    def from_json(cls, json: Any) -> "Info":
        json['first_name'] = str(json['first_name'])
        json['last_name'] = str(json['last_name'])
        json['username'] = str(json['username'])
        del json['first_name']
        del json['last_name']
        del json['username']
        return parse_json(cls, **json)

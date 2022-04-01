from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class Info:

    name: str
    url: str  # AnyUrl
    name: str
    logo_url: str
    logo_thumbnail_url: str
    first_name: str
    last_name: str

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
        return parse_json(cls, **json)

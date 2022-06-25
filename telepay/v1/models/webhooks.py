from dataclasses import dataclass
from typing import Any, List

from ..utils import parse_json


@dataclass
class Webhook:
    id: str
    url: str
    secret: str
    events: List[str]
    active: bool

    @classmethod
    def from_json(cls, json: Any) -> "Webhook":
        return parse_json(cls, **json)


@dataclass
class Webhooks:
    webhooks: List[Webhook]

    def __post_init__(self):
        self.webhooks = [Webhook.from_json(webhook) for webhook in self.webhooks]

    @classmethod
    def from_json(cls, json: Any) -> "Webhooks":
        return parse_json(cls, **json)

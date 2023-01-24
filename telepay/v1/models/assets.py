import logging
from dataclasses import dataclass
from typing import Any, List

from ..utils import parse_json

logger = logging.getLogger(__name__)


@dataclass
class Asset:
    asset: str
    blockchain: str
    usd_price: float
    url: str
    networks: List[str]
    coingecko_id: str

    @classmethod
    def from_json(cls, json: Any) -> "Asset":
        return parse_json(cls, **json)


@dataclass
class Assets:
    assets: List[Asset]

    def __post_init__(self):
        pass

    @classmethod
    def from_json(cls, json: Any) -> "Assets":
        logger.debug(f"Parsing Assets from JSON: {json}")
        return parse_json(cls, **json)

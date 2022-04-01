from os import environ
from dotenv import load_dotenv
from dataclasses import dataclass, field

from .errors import TelePayError


load_dotenv()


@dataclass
class TelePayAuth:
    api_secret: str = field(default=environ["API_SECRET"])

    def __post_init__(self):
        if not self.api_secret:
            raise TelePayError(0, "API_SECRET is not setted")

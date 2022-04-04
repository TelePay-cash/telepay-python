from dataclasses import dataclass, field
from os import environ

from dotenv import load_dotenv

from .errors import TelePayError

load_dotenv()


@dataclass
class TelePayAuth:
    secret_api_key: str = field(default=environ["TELEPAY_SECRET_API_KEY"])

    def __post_init__(self):
        if not self.secret_api_key:
            raise TelePayError(0, "TELEPAY_SECRET_API_KEY is not setted")

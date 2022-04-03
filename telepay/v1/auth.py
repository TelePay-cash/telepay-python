from dataclasses import dataclass, field

from .errors import TelePayError


@dataclass
class TelePayAuth:
    secret_api_key: str

    def __post_init__(self):
        if not self.secret_api_key:
            raise TelePayError(0, "API_SECRET is not setted")

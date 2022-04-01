from dotenv import load_dotenv
from dataclasses import dataclass, field

from .errors import TelePayError


load_dotenv()


@dataclass
class TelePayAuth:
    api_public: str
    api_secret: str

    def __post_init__(self):
        if not self.api_public or not self.api_secret:
            raise TelePayError(0, "API_PUBLIC and API_SECRET must be set in .env")
        if not self.api_public:
            raise TelePayError(0, "API_PUBLIC is not setted")
        if not self.api_secret:
            raise TelePayError(0, "API_SECRET is not setted")

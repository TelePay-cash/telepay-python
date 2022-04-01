from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TelePayError(Exception):
    status_code: int
    status_message: Optional[str] = field(default=None)

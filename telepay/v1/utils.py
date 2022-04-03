from inspect import signature
from typing import Any, Type, TypeVar

from httpx import Response

from .errors import TelePayError

T = TypeVar("T")


def validate_response(response: Response) -> None:
    if response.status_code < 200 or response.status_code >= 300:
        raise TelePayError(status_code=response.status_code, message=response.text)


def parse_json(cls: Type[T], **json: Any) -> T:
    cls_fields = {field for field in signature(cls).parameters}
    native_args, new_args = {}, {}
    for name, val in json.items():
        if name in cls_fields:
            native_args[name] = val
        else:
            new_args[name] = val
    ret = cls(**native_args)
    for new_name, new_val in new_args.items():
        setattr(ret, new_name, new_val)
    return ret

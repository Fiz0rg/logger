from pydantic import ConfigDict
from typing_extensions import TypedDict


class LogDict(TypedDict, total=False):

    # extra="forbid" if field is empty - dont raise error
    __pydantic_config__ = ConfigDict(strict=True, extra="forbid")  # type: ignore allowed

    uuid: str
    message: str
    pri: int
    facility: str
    severity: str
    request_method: str
    uri: str
    host: str
    protocol_version: str
    nginx_timestamp: float
    log_timestamp: float
    geo: dict  # IP, city (short, long)

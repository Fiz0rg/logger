from dataclasses import dataclass

from domain.enum.log import LogLevelEnum


@dataclass
class LogEntity:
    message: str
    ip: str | None = None
    uuid: str | None = None
    geo: dict | None = None
    logLevel: LogLevelEnum | None = None

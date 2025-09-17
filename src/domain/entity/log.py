from pydantic import BaseModel
from typing import Optional, TypedDict
from datetime import datetime


class RawLogDict(TypedDict, total=False):
    uuid: str
    message: str 
    pri: int 
    facility: str
    severity: str 
    request_method: str 
    uri: str 
    host: str
    protocol_version: str
    nginx_timestamp: int
    log_timestamp: int
    ip: str
    geo: int


class LogEntity(BaseModel):
    uuid: Optional[str] = None #+
    message: str # +
    pri: int #+
    facility: str #+
    severity: str #+
    request_method: str #+
    uri: str #+
    host: str # nginx host +
    protocol_version: str #+
    nginx_timestamp: Optional[datetime] = None #+
    log_timestamp: Optional[datetime] = None #+
    ip: Optional[str] = None #+
    geo: Optional[int] = None #+
    # logLevel: Optional[LogLevelEnum] = None 

import ipaddress
import re
from datetime import datetime
from typing import cast
from uuid import uuid4

import IP2Location
from src.domain.entity.log import LogDict
from src.domain.exeption.domain import (
    LogDatetimeError,
    LogGeoError,
    LogIpError,
    LogPriError,
    LogProtocolError,
    LogRequestMethodError,
    LogUriError,
)
from src.domain.exeption.infra import NginxHostError
from src.domain.interfaces.enrich_log import IEnrichLogUsecase
from src.domain.usecase.decorator import wrap_error
from src.infra.const import FACILITY_MAP, SEVERITY_MAP


class EnrichLogUsecase(IEnrichLogUsecase):
    def enrich(self, log: str) -> LogDict:
        nginx_info, log_payload = self._split_nginx_log(log=log)

        lg = cast(LogDict, {})
        lg["message"] = log

        lg = self._parse_log_payload(log_payload=log_payload, log_dict=lg)
        lg = self._parse_nginx_info(nginx_info=nginx_info, log_dict=lg)

        return lg

    def _parse_log_payload(self, *, log_payload: str, log_dict: LogDict) -> LogDict:

        ip = self._parse_ip(log_payload=log_payload)
        self._parse_geo(log_dict=log_dict, ip=ip)

        # log datetime
        dt = re.search(r"\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]", log_payload)
        try:
            if dt is not None:
                dt = dt.group(1)
                dt = datetime.strptime(dt, "%d/%b/%Y:%H:%M:%S %z")
                timestamp = dt.timestamp()
                log_dict["log_timestamp"] = timestamp
        except Exception as err:
            raise LogDatetimeError(msg="Log datetime error") from err

        # request_method
        request_method = re.search(r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)", log_payload)
        try:
            if request_method is not None:
                request_method = request_method.group()
                log_dict["request_method"] = request_method
        except Exception as err:
            raise LogRequestMethodError(msg="Log request method error") from err

        # protocot version
        protocol_version = re.search(r"HTTP/\d\.\d", log_payload)
        try:
            if protocol_version is not None:
                protocol_version = protocol_version.group()
                log_dict["protocol_version"] = protocol_version
        except Exception as err:
            raise LogProtocolError(msg="Log protocol error") from err

        # URI
        uri = re.search(r'"[A-Z]+ ([^ ]+) HTTP/\d\.\d"', log_payload)
        try:
            if uri is not None:
                uri = uri.group(1)
                log_dict["uri"] = uri
        except Exception as err:
            raise LogUriError(msg="Log uri error") from err

        # uuid
        uuid = str(uuid4())
        log_dict["uuid"] = uuid

        return log_dict

    def _parse_nginx_info(self, *, nginx_info: str, log_dict: LogDict) -> LogDict:

        # PRI
        pri = re.search(r"<(\d+)>", nginx_info)
        try:
            if pri is not None:
                pri = int(pri.group(1))
                log_dict["pri"] = pri

                facility = FACILITY_MAP[pri // 8]
                log_dict["facility"] = facility

                severity = SEVERITY_MAP[pri % 6]
                log_dict["severity"] = severity
        except Exception as err:
            raise LogPriError(msg="PRI doesnt find") from err

        # datetime
        dt = re.search(r"\b[A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2}\b", nginx_info)
        try:
            if dt is not None:
                dt = dt.group()
                year = datetime.now().year
                dt = datetime.strptime(f"{year} {dt}", "%Y %b %d %H:%M:%S")
                timestamp = dt.timestamp()
                log_dict["nginx_timestamp"] = timestamp
        except Exception as err:
            raise LogDatetimeError(msg="NGINX datetime error") from err

        # host
        host = re.search(r"\d{2}:\d{2}:\d{2} (\S+) nginx:", nginx_info)
        try:
            if host is not None:
                host = host.group()
                log_dict["host"] = host
        except Exception as err:
            raise NginxHostError(msg="Nginx host error") from err

        return log_dict

    def _split_nginx_log(self, *, log: str) -> tuple[str, str]:
        separate_nginx_from_log = log.split(" nginx: ")
        nginx_info = separate_nginx_from_log[0]
        log_payload = separate_nginx_from_log[1]
        return nginx_info, log_payload

    @wrap_error(err_class=LogGeoError, err_message="GEO gettings error")
    def _parse_geo(self, log_dict: LogDict, ip: str) -> LogDict:
        db = IP2Location.IP2Location("IP2LOCATION-LITE-DB1.IPV6.BIN")
        geo = db.get_all(ip)
        geo = geo.__dict__
        log_dict["geo"] = geo
        return log_dict

    @wrap_error(err_class=LogIpError, err_message="String is not valid IP address")
    def _parse_ip(self, log_payload: str) -> str:
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log_payload)
        if ip is None:
            raise LogIpError(msg="IP address doesnt exist")
        ip = ip.group()
        ipaddress.ip_address(ip)
        return ip

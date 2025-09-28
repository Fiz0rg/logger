import ipaddress
import re
from datetime import datetime
from typing import cast
from uuid import uuid4

import IP2Location

from src.domain.entity.log import LogDict
from src.domain.interfaces.enrich_log import IEnrichLogUsecase
from src.infra.const import FACILITY_MAP, SEVERITY_MAP


class EnrichLogUsecase(IEnrichLogUsecase):
    async def enrich(self, log: str) -> LogDict:
        nginx_info, log_payload = self._split_nginx_log(log=log)

        lg = cast(LogDict, {})
        lg["message"] = log

        lg = self._parse_log_payload(log_payload=log_payload, log_dict=lg)
        lg = self._parse_nginx_info(nginx_info=nginx_info, log_dict=lg)

        return lg

    def _parse_log_payload(self, *, log_payload: str, log_dict: LogDict) -> LogDict:

        # IP
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log_payload)
        if ip is not None:
            ip = ip.group()
        else:
            raise BaseException("IP doesnt find")

        try:
            ipaddress.ip_address(ip)
        except Exception as err:
            raise ValueError("String is not IP address") from err

        # GEO
        try:
            db = IP2Location.IP2Location("IP2LOCATION-LITE-DB1.IPV6.BIN")
            geo = db.get_all(ip)
            geo = geo.__dict__
            log_dict["geo"] = geo
        except Exception as err:
            raise BaseException("GEO gettings error") from err

        # log datetime
        dt = re.search(r"\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]", log_payload)
        if dt is not None:
            dt = dt.group(1)
            dt = datetime.strptime(dt, "%d/%b/%Y:%H:%M:%S %z")
            timestamp = dt.timestamp()
            log_dict["log_timestamp"] = timestamp

        # request_method
        request_method = re.search(r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)", log_payload)
        if request_method is not None:
            request_method = request_method.group()
            log_dict["request_method"] = request_method

        # protocot version
        protocol_version = re.search(r"HTTP/\d\.\d", log_payload)
        if protocol_version is not None:
            protocol_version = protocol_version.group()
            log_dict["protocol_version"] = protocol_version

        # URI
        uri = re.search(r'"[A-Z]+ ([^ ]+) HTTP/\d\.\d"', log_payload)
        if uri is not None:
            uri = uri.group(1)
            log_dict["uri"] = uri

        # uuid
        uuid = str(uuid4())
        log_dict["uuid"] = uuid

        return log_dict

    def _parse_nginx_info(self, *, nginx_info: str, log_dict: LogDict) -> LogDict:

        # PRI
        pri = re.search(r"<(\d+)>", nginx_info)
        if pri is not None:
            pri = int(pri.group(1))
            log_dict["pri"] = pri
        else:
            raise BaseException("PRI doesnt find")

        facility = FACILITY_MAP[pri // 8]
        log_dict["facility"] = facility

        severity = SEVERITY_MAP[pri % 6]
        log_dict["severity"] = severity

        # datetime
        dt = re.search(r"\b[A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2}\b", nginx_info)
        if dt is not None:
            dt = dt.group()
            year = datetime.now().year
            dt = datetime.strptime(f"{year} {dt}", "%Y %b %d %H:%M:%S")
            timestamp = dt.timestamp()
            log_dict["nginx_timestamp"] = timestamp

        host = re.search(r"\d{2}:\d{2}:\d{2} (\S+) nginx:", nginx_info)
        if host is not None:
            host = host.group()
            log_dict["host"] = host

        return log_dict

    def _split_nginx_log(self, *, log: str) -> tuple[str, str]:
        separate_nginx_from_log = log.split(" nginx: ")
        nginx_info = separate_nginx_from_log[0]
        log_payload = separate_nginx_from_log[1]
        return nginx_info, log_payload

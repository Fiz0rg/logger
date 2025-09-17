import asyncio
import ipaddress
import re
import IP2Location

from uuid import uuid4
from datetime import datetime

from asyncio import StreamReader, StreamWriter
from src.infra.config import settings
from src.infra.const import FACILITY_MAP, SEVERITY_MAP

class ParseLog:
    def __init__(self, log: str) -> None:
        self.log = log

    def exec(self):
        nginx_info, log_payload = self._split_nginx_log()

        self._parse_log_payload(log_payload=log_payload)
        self._parse_nginx_info(nginx_info=nginx_info)


    def _parse_log_payload(self, *, log_payload: str): 

        # IP
        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log_payload)
        if ip is not None:
            ip = ip.group()
        else:
            raise BaseException("IP doesnt find")
        
        try:
            ipaddress.ip_address(ip)
        except:
            raise ValueError("String is not IP address")
        
        try:
            db = IP2Location.IP2Location("IP2LOCATION-LITE-DB1.IPV6.BIN")
            geo = db.get_all(ip)
            print(f"{geo=}")
        except:
            raise BaseException("GEO gettings error")

        
        #datetime
        dt = re.search(r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]', log_payload)
        if dt is not None:
            dt = dt.group(1)
            dt = datetime.strptime(dt, "%d/%b/%Y:%H:%M:%S %z")
            timestamp = dt.timestamp()

        # request_method
        request_method = re.search(r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)", log_payload)
        if request_method is not None:
            request_method = request_method.group()

        protocol_version = re.search(r"HTTP/\d\.\d", log_payload)
        if protocol_version is not None:
            protocol_version = protocol_version.group()

        uri = re.search(r'"[A-Z]+ ([^ ]+) HTTP/\d\.\d"', log_payload)
        if uri is not None:
            uri = uri.group(1)
            print(f'{uri=}')

        #uuid 
        uuid = str(uuid4())
        print(f'{uuid=}')   


    def _parse_nginx_info(self, *, nginx_info: str):
        pri = re.search(r"<(\d+)>", nginx_info)
        if pri is not None:
            pri = int(pri.group(1))
        else:
            raise BaseException("PRI doesnt find")
        
        facility = FACILITY_MAP[pri // 8]
        severity = SEVERITY_MAP[pri % 6]

        #datetime
        dt = re.search(r'\b[A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2}\b', nginx_info)
        if dt is not None:
            dt = dt.group()
            year = datetime.now().year
            dt = datetime.strptime(f"{year} {dt}", "%Y %b %d %H:%M:%S")
            timestamp = dt.timestamp()


    def _split_nginx_log(self) -> tuple[str, str]:
        separate_nginx_from_log = self.log.split(" nginx: ")
        nginx_info = separate_nginx_from_log[0]
        log_payload = separate_nginx_from_log[1]
        return nginx_info, log_payload
    


    

    


# НАЙТИ МЕСТО!
def parse_log(log: str):
    a = ParseLog(log=log)
    b = a.exec()
    
    


async def handle_connection(reader: StreamReader, writer: StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"Подключение от {addr}")
    data = await reader.read(1024)
    message = data.decode()
    _ = parse_log(message)



async def main():
    server = await asyncio.start_server(handle_connection, settings.HOST, settings.PORT)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f'WTF {addrs=}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())


# from user_agents import parse
    # item = [i for i in message if "User-Agent" in i]
    # res = item[0].split(":")[1]
    # pa = parse(res)

    # device_data = {
    #     "browser": pa.browser.family,
    #     "os": pa.os.family,
    #     "device": pa.device.family,
    #     "is_mobile": pa.is_mobile,
    # }

    # # print(f"{device_data=}")

    # try:
    #     with geoip2.database.Reader("GeoLite2-Country.mmdb") as geodb:
    #         try:
    #             ip = "193.232.92.0"
    #             some = geodb.country(ip)
    #             print(some.country.name)
    #         except geoip2.errors.AddressNotFoundError:
    #             print("IP не найден в базе")
    # except FileNotFoundError:
    #     print("Файл базы данных не найден")



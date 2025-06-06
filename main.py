from asyncio import StreamReader, StreamWriter, run, start_server

import geoip2.database
import geoip2.errors
from user_agents import parse


async def handle_connection(reader: StreamReader, writer: StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"Подключение от {addr}")
    data = await reader.read(1024)
    message = data.decode().splitlines()
    print(f"{message=}")

    item = [i for i in message if "User-Agent" in i]
    res = item[0].split(":")[1]
    pa = parse(res)

    device_data = {
        "browser": pa.browser.family,
        "os": pa.os.family,
        "device": pa.device.family,
        "is_mobile": pa.is_mobile,
    }

    print(f"{device_data=}")

    try:
        with geoip2.database.Reader("GeoLite2-Country.mmdb") as geodb:
            try:
                ip = "193.232.92.0"
                some = geodb.country(ip)
                print(some.country.name)
            except geoip2.errors.AddressNotFoundError:
                print("IP не найден в базе")
    except FileNotFoundError:
        print("Файл базы данных не найден")


async def main():
    server = await start_server(handle_connection, "127.0.0.1", port=8080)  # ПЕРЕДЕЛАТЬ ПОД ENV

    async with server:
        await server.serve_forever()

    print("!@#")


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен вручную.")

import asyncio
from asyncio import StreamReader, StreamWriter

from src.application.enrich_logs import LogProcessingOrchestrator
from src.application.validator import LogValidator
from src.domain.usecase.enrich_log import EnrichLogUsecase
from src.infra.config import settings
from src.infra.kafka import EventBus


# НАЙТИ МЕСТО!
async def parse_log(log: str):
    enricher = EnrichLogUsecase()
    validator = LogValidator()
    event_bus = EventBus()

    lpo = LogProcessingOrchestrator(enricher=enricher, validator=validator, event_bus=event_bus)
    _ = await lpo.execute(raw_log=log)


async def handle_connection(reader: StreamReader, writer: StreamWriter):
    addr = writer.get_extra_info("peername")
    data = await reader.read(1024)
    message = data.decode()
    _ = await parse_log(message)


async def main():
    server = await asyncio.start_server(handle_connection, settings.HOST, settings.PORT)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

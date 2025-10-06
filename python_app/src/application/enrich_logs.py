from json import dumps

from src.domain.interfaces.enrich_log import IEnrichLogUsecase
from src.domain.interfaces.event_bus import iEventBus
from src.domain.interfaces.validator import ILogValidator


class LogProcessingOrchestrator:
    def __init__(self, *, event_bus: iEventBus, enricher: IEnrichLogUsecase, validator: ILogValidator) -> None:
        self.event_bus = event_bus
        self.enricher = enricher
        self.validator = validator

    async def execute(self, *, raw_log: str) -> None:

        enriched_log = self.enricher.enrich(log=raw_log)

        log, is_valid = self.validator.is_satisfied(log=enriched_log)

        if is_valid is True:
            topic = "test"
            message = dumps(log)
            self.event_bus.publish(topic=topic, message=message)

        self.event_bus.consume(topic="test")

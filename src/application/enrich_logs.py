from domain.interfaces.event_bus import iEventBus


class EnrichLogHandler:
    def __init__(self, event_bus: iEventBus) -> None:
        self.event_bus = event_bus

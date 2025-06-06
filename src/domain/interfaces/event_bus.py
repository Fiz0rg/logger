from abc import ABC, abstractmethod


class iEventBus(ABC):
    @abstractmethod
    def publish(self, topic: str, message: str) -> None: ...

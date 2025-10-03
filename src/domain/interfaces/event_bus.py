from abc import ABC, abstractmethod


class iEventBus(ABC):
    @abstractmethod
    def publish(self, *, topic: str, message: str) -> None: ...

    @abstractmethod
    def healthcheck(self) -> None: ...

    @abstractmethod
    def consume(self, *, topic: str) -> None: ...

from abc import ABC, abstractmethod

from domain.entity.log import LogEntity


class ILogService(ABC):
    @abstractmethod
    def generate(self, log: LogEntity) -> LogEntity: ...

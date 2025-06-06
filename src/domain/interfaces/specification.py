from abc import ABC, abstractmethod

from domain.entity.log import LogEntity


class ILogSpecification(ABC):
    @abstractmethod
    def is_satisfied(self, log: LogEntity) -> LogEntity: ...

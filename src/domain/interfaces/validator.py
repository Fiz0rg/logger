from abc import ABC, abstractmethod

from src.domain.entity.log import LogDict


class ILogValidator(ABC):
    @abstractmethod
    def is_satisfied(self, log: LogDict) -> tuple[LogDict, bool]: ...

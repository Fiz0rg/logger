from abc import ABC, abstractmethod

from src.domain.entity.log import LogDict


class IEnrichLogUsecase(ABC):
    @abstractmethod
    def enrich(self, log: str) -> LogDict: ...

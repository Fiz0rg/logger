from domain.interfaces.log_service import ILogService
from domain.interfaces.specification import ILogSpecification
from src.domain.entity.log import LogEntity


class Result:
    item: LogEntity


class UsecaseSpecification(ILogSpecification):
    def __init__(self, *specs):
        self.specs = specs


class EnrichLogUsecase:
    def __init__(self, uuid_service: ILogService, geo_service: ILogService) -> None:
        self.uuid_service = uuid_service
        self.geo_service = geo_service

    async def __call__(self, log: LogEntity) -> None: ...

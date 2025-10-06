from pydantic import TypeAdapter
from src.domain.entity.log import LogDict
from src.domain.interfaces.validator import ILogValidator


class LogValidator(ILogValidator):
    def is_satisfied(self, log: LogDict) -> tuple[LogDict, bool]:

        adapter = TypeAdapter(LogDict)

        try:
            adapter.validate_python(log)
        except Exception as err:
            raise ValueError("Log validation error") from err

        # raise ValueError("CHECK HOST IN NGINX LOG")
        return log, True

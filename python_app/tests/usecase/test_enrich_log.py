import pytest
from src.domain.exeption.domain import LogIpError
from src.domain.usecase.enrich_log import EnrichLogUsecase
from tests.conftest import make_log


# pytest tests/usecase/test_enrich_log.py::test_enrich_ok -v -s
def test_enrich_ok():
    log = make_log()
    uc = EnrichLogUsecase()
    res = uc.enrich(log=log)

    assert isinstance(res, dict)


# pytest tests/usecase/test_enrich_log.py::test_enrich_log_IP_exclude_error -v -s
def test_enrich_log_IP_exclude_error():
    exclude = ["ip"]
    log = make_log(exclude=exclude)
    uc = EnrichLogUsecase()
    with pytest.raises(LogIpError) as err:
        uc.enrich(log=log)

    assert "IP address doesnt exist" in str(err.value)


# pytest tests/usecase/test_enrich_log.py::test_enrich_log_IP_wrong_IP_string -v -s
def test_enrich_log_IP_wrong_IP_string():
    override = {"ip": "999.999.999.999"}
    log = make_log(overrides=override)
    uc = EnrichLogUsecase()
    with pytest.raises(LogIpError) as err:
        uc.enrich(log=log)

    assert "String is not valid IP address" in str(err.value)

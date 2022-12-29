import pytest

from src.bootstrap import bootstrap
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import AiosqliteUnitOfWork


@pytest.fixture
def in_memory_sqlite_db():
    """
    Method to get in memory sqlite db
    :return: str
    """
    return ':memory:'


@pytest.fixture
def aiosqlite_bus(in_memory_sqlite_db):
    bus = bootstrap(
        uow=AiosqliteUnitOfWork()
    )
    yield bus

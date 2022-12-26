import pathlib

import pytest
import tempfile


@pytest.fixture
def in_memory_sqlite_db():
    """
    Method to get in memory sqlite db
    :return: str
    """
    return ':memory:'


@pytest.fixture
def get_fake_csv_tables_names():
    """
    Returns temp paths of csv files.
    :return: Dict[str, str]
    """
    temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    db_path = pathlib.Path(temp_dir.name)
    names = ['cats.csv']
    return temp_dir, {name[:name.find('.')]: str(db_path / name) for name in names}

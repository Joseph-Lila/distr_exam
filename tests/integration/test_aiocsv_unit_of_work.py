import os
import pathlib
import tempfile
import shutil

import aiofiles
import pytest

from domain.models import Cat
from service_layer.unit_of_work.aiocsv_unit_of_work import AiocsvUnitOfWork


@pytest.mark.asyncio
async def test_transaction(get_fake_csv_tables_names):
    temp_dir, fake_csv_tables_names = get_fake_csv_tables_names
    try:
        uow = AiocsvUnitOfWork(paths=fake_csv_tables_names)
        async with uow:
            assert type(temp_dir.name) == str
    finally:
        temp_dir.cleanup()

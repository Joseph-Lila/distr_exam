import asyncio
import os
import pathlib
import tempfile
import shutil
from typing import List, Optional

import aiofiles
import pytest

from adapters.aiocsv.create_db import create_tables
from domain.models import Cat, BaseEntity
from service_layer.unit_of_work.aiocsv_unit_of_work import AiocsvUnitOfWork


@pytest.mark.asyncio
async def test_transaction(get_fake_csv_tables_names):
    temp_dir, fake_csv_tables_names = get_fake_csv_tables_names
    await create_tables(fake_csv_tables_names)
    try:
        uow = AiocsvUnitOfWork(paths=fake_csv_tables_names)
        async with uow:
            assert type(temp_dir.name) == str
    finally:
        temp_dir.cleanup()


@pytest.mark.asyncio
async def test_creation(get_fake_csv_tables_names):
    temp_dir, fake_csv_tables_names = get_fake_csv_tables_names
    await create_tables(fake_csv_tables_names)
    new_item = Cat(nick='Кот в сапогах')
    try:
        uow = AiocsvUnitOfWork(paths=fake_csv_tables_names)
        async with uow:
            # fill the tables
            await uow.cats.create(new_item)
            await uow.commit()
            cats: List[BaseEntity] = await uow.cats.get_all()
            assert len(cats) == 1
    finally:
        temp_dir.cleanup()


@pytest.mark.asyncio
async def test_getting_all(get_fake_csv_tables_names):
    temp_dir, fake_csv_tables_names = get_fake_csv_tables_names
    await create_tables(fake_csv_tables_names)
    new_items = [Cat(nick='Кот в сапогах'), Cat(nick='Лилия')]
    try:
        uow = AiocsvUnitOfWork(paths=fake_csv_tables_names)
        async with uow:
            # fill the tables
            for item in new_items:
                await uow.cats.create(item)
            await uow.commit()
            # check data
            cats = await uow.cats.get_all()
            assert len(cats) == 2
            assert cats[0].item_id == 1
            assert cats[1].item_id == 2
    finally:
        temp_dir.cleanup()


@pytest.mark.asyncio
async def test_getting_one(get_fake_csv_tables_names):
    temp_dir, fake_csv_tables_names = get_fake_csv_tables_names
    await create_tables(fake_csv_tables_names)
    new_item = Cat(nick='Кот в сапогах')
    try:
        uow = AiocsvUnitOfWork(paths=fake_csv_tables_names)
        async with uow:
            # fill the tables
            await uow.cats.create(new_item)
            await uow.commit()
            # check data
            cat = await uow.cats.get_by_id(1)
            assert cat is not None
            assert cat.nick == new_item.nick
    finally:
        temp_dir.cleanup()

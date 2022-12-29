from typing import Optional

import pytest

from src.domain.models import MusicFavor, BaseEntity
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import AiosqliteUnitOfWork
from src.adapters.repository.aiosqlite.create_db import CREATE_MUSIC_FAVORS_TABLE


@pytest.mark.asyncio
async def test_transaction(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        assert in_memory_sqlite_db == ':memory:'


@pytest.mark.asyncio
async def test_creation(in_memory_sqlite_db):
    new_item = MusicFavor()
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)  # each time we connect to new in-memory db
        await uow.commit()  # so that we need to create tables for each __aenter__ entry
        assert uow.conn.total_changes == 0
        await uow.music_favors.create(new_item)
        assert uow.conn.total_changes > 0


@pytest.mark.asyncio
async def test_getting_all(in_memory_sqlite_db):
    new_items = [MusicFavor(), MusicFavor(group_name='Abba')]
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        for item in new_items:
            await uow.music_favors.create(item)
        await uow.commit()
        # check data
        music_favors = await uow.music_favors.get_all()
        assert len(music_favors) == 2
        assert music_favors[0].item_id == 1
        assert music_favors[1].item_id == 2


@pytest.mark.asyncio
async def test_getting_one(in_memory_sqlite_db):
    new_item = MusicFavor()
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        await uow.music_favors.create(new_item)
        await uow.commit()
        # check data
        music_favor: Optional[BaseEntity] = await uow.music_favors.get_by_id(1)
        assert music_favor is not None
        assert music_favor.group_name == new_item.group_name

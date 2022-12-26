from typing import Optional

import pytest

from adapters.aiosqlite.create_db import CREATE_MUSIC_FAVORS_TABLE
from domain.models import Cat, BaseEntity
from service_layer.unit_of_work.aiosqlite_unit_of_work import \
    AiosqliteUnitOfWork


@pytest.mark.asyncio
async def test_transaction(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        assert in_memory_sqlite_db == ':memory:'


@pytest.mark.asyncio
async def test_creation(in_memory_sqlite_db):
    new_item = Cat(nick='Кот в сапогах')
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)  # each time we connect to new in-memory db
        await uow.commit()  # so that we need to create tables for each __aenter__ entry
        assert uow.conn.total_changes == 0
        await uow.cats.create(new_item)
        assert uow.conn.total_changes > 0


@pytest.mark.asyncio
async def test_getting_all(in_memory_sqlite_db):
    new_items = [Cat(nick='Кот в сапогах'), Cat(nick='Лилия')]
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        for item in new_items:
            await uow.cats.create(item)
        await uow.commit()
        # check data
        cats = await uow.cats.get_all()
        assert len(cats) == 2
        assert cats[0].item_id == 1
        assert cats[1].item_id == 2


@pytest.mark.asyncio
async def test_getting_one(in_memory_sqlite_db):
    new_item = Cat(nick='Кот в сапогах')
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        await uow.cats.create(new_item)
        await uow.commit()
        # check data
        cat = await uow.cats.get_by_id(1)
        assert cat is not None
        assert cat.nick == new_item.nick


@pytest.mark.asyncio
async def test_updating(in_memory_sqlite_db):
    new_item = Cat(nick='Кот в сапогах')
    new_nick = 'John'
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        await uow.cats.create(new_item)
        await uow.commit()
        # check data
        cat = await uow.cats.get_by_id(1)
        assert cat.nick == new_item.nick
        cat.nick = new_nick
        await uow.cats.update(cat)
        cat = await uow.cats.get_by_id(1)
        assert cat.nick == new_nick


@pytest.mark.asyncio
async def test_deleting(in_memory_sqlite_db):
    new_item = Cat(nick='Кот в сапогах')
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        # create tables
        await uow.conn.execute(CREATE_MUSIC_FAVORS_TABLE)
        await uow.commit()
        # fill the tables
        await uow.cats.create(new_item)
        await uow.commit()
        # check data
        cat: Optional[Cat] = await uow.cats.get_by_id(1)
        assert cat is not None
        await uow.cats.delete(cat.item_id)
        await uow.commit()
        cat: Optional[Cat] = await uow.cats.get_by_id(1)
        assert cat is None

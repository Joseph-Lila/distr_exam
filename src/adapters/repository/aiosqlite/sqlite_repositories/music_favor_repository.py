""" Module adapters.sqlite_repositories.music_favor_repository """
from typing import List, Optional

from src.adapters.repository.abstract_repository import AbstractRepository
from src.domain import models
from src.domain.models import MusicFavor


class MusicFavorRepository(AbstractRepository):
    """ Music Favor Repository class implementation """

    def __init__(self, session):
        self.session = session

    async def get_all(self) -> List[models.BaseEntity]:
        items = []
        async with self.session.execute(
                "SELECT * FROM music_favors;"
        ) as cursor:
            async for row in cursor:
                items.append(MusicFavor(*row))
        return items

    async def get_by_id(self, item_id: int) -> Optional[models.BaseEntity]:
        cursor = await self.session.execute(
            "SELECT * "
            "FROM music_favors "
            "WHERE item_id = ?;",
            (item_id,)
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return MusicFavor(*row)

    async def update(self, item):
        raise NotImplementedError

    async def delete(self, item_id: int):
        raise NotImplementedError

    async def create(self, item):
        await self.session.execute(
            "INSERT INTO music_favors "
            "(group_name, country, mentor_surname, written_disks_quantity, total_disks_quantity) "
            "values (?, ?, ?, ?, ?);",
            (item.group_name, item.country, item.mentor_surname, item.written_disks_quantity, item.total_disks_quantity)
        )


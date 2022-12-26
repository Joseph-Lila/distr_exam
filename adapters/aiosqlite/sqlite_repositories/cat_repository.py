""" Module adapters.sqlite_repositories.cat_repository """
from typing import List, Optional

from adapters.abstract_repository import \
    AbstractRepository
from domain import models
from domain.models import Cat


class CatRepository(AbstractRepository):
    """ Cat Repository class implementation """

    def __init__(self, session):
        self.session = session

    async def get_all(self) -> List[models.BaseEntity]:
        items = []
        async with self.session.execute(
            "SELECT * FROM cats;"
        ) as cursor:
            async for row in cursor:
                items.append(Cat(*row))
        return items

    async def get_by_id(self, item_id: int) -> Optional[models.BaseEntity]:
        cursor = await self.session.execute(
            "SELECT * "
            "FROM cats "
            "WHERE item_id = ?;",
            (item_id,)
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return Cat(*row)

    async def update(self, item):
        await self.session.execute(
            "UPDATE cats "
            "SET nick = ? "
            "WHERE item_id = ?;",
            (item.nick, item.item_id)
        )

    async def delete(self, item_id: int):
        await self.session.execute(
            "DELETE FROM cats "
            "WHERE item_id = ?;",
            (item_id,)
        )

    async def create(self, item: Cat):
        await self.session.execute(
            "INSERT INTO cats (nick) values (?);",
            (item.nick,)
        )

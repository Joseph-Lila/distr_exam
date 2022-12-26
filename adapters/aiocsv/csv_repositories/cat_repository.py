import csv
from typing import List, Optional

import aiofiles
import loguru
from aiocsv import AsyncWriter, AsyncReader, AsyncDictReader, AsyncDictWriter

from adapters.abstract_repository import AbstractRepository
from domain import models
from domain.models import Cat, BaseEntity
from dataclasses import asdict


class CatRepository(AbstractRepository):

    def __init__(self, path, header):
        self.path = path
        self.header: tuple = header

    async def get_all(self) -> List[models.BaseEntity]:
        cats = []
        async with aiofiles.open(self.path, mode="r", encoding="utf-8", newline="") as afp:
            async for row in AsyncDictReader(afp):
                cats.append(Cat(item_id=int(row.get('item_id')), nick=row['nick']))
        return cats

    async def get_by_id(self, item_id: int) -> Optional[models.BaseEntity]:
        async with aiofiles.open(self.path, mode="r", encoding="utf-8", newline="") as afp:
            async for row in AsyncDictReader(afp):
                if int(row.get('item_id', None)) == item_id:
                    return Cat(item_id=int(row.get('item_id')), nick=row['nick'])

    async def update(self, item):
        pass

    async def delete(self, item_id: int):
        pass

    async def create(self, item: BaseEntity):
        item.item_id = await self._get_next_id(item)
        async with aiofiles.open(self.path, mode="a", encoding="utf-8", newline="") as afp:
            writer = AsyncDictWriter(afp, self.header, restval="NULL", quoting=csv.QUOTE_ALL)
            await writer.writerow(asdict(item))
        from loguru import logger
        logger.info(asdict(item))

    async def _get_next_id(self, item: BaseEntity):
        cats = await self.get_all()
        if len(cats) == 0:
            return 1
        else:
            return int(cats[-1].item_id) + 1

from typing import List

from adapters.abstract_repository import AbstractRepository
from domain import models


class CatRepository(AbstractRepository):

    def __init__(self, writer, header):
        self.writer = writer
        self.header = header

    async def get_all(self) -> List[models.BaseEntity]:
        pass

    async def get_by_id(self, item_id: int) -> models.BaseEntity:
        pass

    async def update(self, item):
        pass

    async def delete(self, item_id: int):
        pass

    async def create(self, item):
        pass

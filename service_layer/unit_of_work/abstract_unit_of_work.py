""" Module src.unit_of_work """
import abc
from typing import Optional

from adapters.abstract_repository import AbstractRepository
from adapters.aiosqlite.sqlite_repositories.cat_repository import CatRepository


class AbstractUnitOfWork(abc.ABC):
    """
    Abstract class for `unit of work` realizations.
    """
    music_favors: Optional[AbstractRepository]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        """
        Method to confirm changes
        :return:
        """
        await self._commit()

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        """
        Method to rollback changes
        :return:
        """
        raise NotImplementedError

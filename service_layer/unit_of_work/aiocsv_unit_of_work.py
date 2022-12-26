import csv
from typing import List, Optional, Dict

import aiofiles
from aiocsv import AsyncDictWriter, AsyncDictReader

from adapters.aiocsv.csv_repositories.cat_repository import CatRepository
from config import get_csv_headers, get_csv_tables_names
from service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


class AiocsvUnitOfWork(AbstractUnitOfWork):

    def __init__(self, paths: Optional[Dict[str, str]] = get_csv_tables_names(), headers=get_csv_headers()):
        super().__init__()
        self._paths: Optional[Dict[str, str]] = paths
        self._headers = headers

    @property
    def conn(self):
        """
        Readonly property to get connections.
        :return:
        """
        return self._paths, self._headers

    async def __aenter__(self):
        self.cats = CatRepository(self._paths['cats'], self._headers['cats'])
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(self, *args)
        self.cats = None

    async def _commit(self):
        """
        It is pretty difficult to make commit for csv.
        So that this method doesn't do anything.
        :return: None
        """

    async def rollback(self):
        """
        It is pretty difficult to make rollback for csv.
        So that this method doesn't do anything.
        :return: None
        """

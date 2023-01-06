import asyncio
import functools

import asynckivy as ak

from src.domain.commands import (AddMusicFavor, GetDbDataFromServer,
                                 GetMusicFavors, GetMusicFavorsBySubstring,
                                 SendDbDataToServer)
from src.domain.events import (DataIsGiven, DbDataIsSentFromServer,
                               DbDataIsSentToServer, MadeRequest)
from src.domain.utilities import get_message, send_message
from src.entrypoints.client.views.data_screen.data_screen import DataScreenView


def use_loop(func):
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(func(self, *args, **kwargs))

    return wrapped


class DataScreenController:
    def __init__(self, client, main_controller):
        self.client = client
        self._view = DataScreenView(
            controller=self,
            main_controller=main_controller
        )

    def get_view(self):
        return self._view

    @use_loop
    async def send_add_command(self, new_item):
        try:
            await send_message(AddMusicFavor(new_item), self.client.writer)
            await get_message(self.client.reader)
            ak.start(self.send_get_data_command())
        except Exception:
            self._view.show_lost_connection_snackbar()

    @use_loop
    async def send_get_data_command(self):
        try:
            await send_message(GetMusicFavors(), self.client.writer)
            response: DataIsGiven = await get_message(self.client.reader)
            await self._view.data_is_given(response.data)
        except Exception:
            self._view.show_lost_connection_snackbar()

    @use_loop
    async def send_request_command(self, substr: str):
        try:
            await send_message(GetMusicFavorsBySubstring(substr), self.client.writer)
            response: MadeRequest = await get_message(self.client.reader)
            await self._view.data_is_given(response.data)
        except Exception:
            self._view.show_lost_connection_snackbar()

    @use_loop
    async def export_database(self, *args):
        response = await self.client.share_additional_db()
        try:
            await send_message(SendDbDataToServer(response.data), self.client.writer)
            await get_message(self.client.reader)
            await self.send_get_data_command()
            self._view.show_snackdar("Data exported successfully!")
        except Exception:
            self._view.show_lost_connection_snackbar()

    @use_loop
    async def import_database(self, *args):
        try:
            await send_message(GetDbDataFromServer(), self.client.writer)
            response: DbDataIsSentFromServer = await get_message(self.client.reader)
            await self.client.fill_additional_db(response)
            await self.send_get_data_command()
            self._view.show_snackdar("Data imported successfully!")
        except Exception:
            self._view.show_lost_connection_snackbar()

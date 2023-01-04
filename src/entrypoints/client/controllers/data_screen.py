import asyncio
import functools
import asynckivy as ak
from src.domain.commands import AddMusicFavor, GetMusicFavors
from src.domain.events import DataIsGiven
from src.domain.utilities import send_message, get_message
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

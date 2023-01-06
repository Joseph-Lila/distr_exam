from src.domain.commands import GetMusicFavors, SendDbDataToServer
from src.domain.events import DataIsGiven
from src.domain.utilities import get_message, send_message
from src.entrypoints.client.controllers.data_screen import use_loop
from src.entrypoints.client.views.pandas_screen.pandas_screen import \
    PandasScreenView


class PandasScreenController:
    def __init__(self, client, main_controller):
        self.client = client
        self._view = PandasScreenView(
            controller=self,
            main_controller=main_controller
        )

    def get_view(self):
        return self._view

    @use_loop
    async def send_get_data_command(self):
        try:
            await send_message(GetMusicFavors(), self.client.writer)
            response: DataIsGiven = await get_message(self.client.reader)
            await self._view.data_is_given(response.data)
        except Exception:
            self._view.show_lost_connection_snackbar()

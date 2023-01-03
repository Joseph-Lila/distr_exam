import asyncio
from typing import Optional
from functools import partial
from src.domain.utilities import Client
from src.entrypoints.client.views.connection_screen.connection_screen import ConnectionScreenView


class ConnectionScreenController:
    def __init__(self, client, main_controller):
        self.client = client
        self._view = ConnectionScreenView(
            controller=self,
            main_controller=main_controller
        )
        self._init_view()

    def get_view(self):
        return self._view

    def _init_view(self):
        self._view.host.text = self.client.host
        self._view.port.text = str(self.client.port)

    def _check_client(self, *args):
        new_state = args[0]
        if self.client.connected and new_state == Client.CONNECTED:
            self._view.connected()
        elif not self.client.connected and new_state == Client.DISCONNECTED:
            self._view.disconnected()

    async def change_state(self, new_state: str, host: Optional[str] = None, port: Optional[int] = None):
        if new_state == Client.CONNECTED:
            self.client.host = host
            self.client.port = port

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            if new_state == Client.CONNECTED:
                task = loop.create_task(self.client.connect())
            else:
                task = loop.create_task(self.client.disconnect())
            task.add_done_callback(partial(self._check_client, new_state))

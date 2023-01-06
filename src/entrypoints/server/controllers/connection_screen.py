import asyncio
from functools import partial
from typing import Optional

from src.domain.utilities import Server
from src.entrypoints.server.views.connection_screen.connection_screen import \
    ConnectionScreenView


class ConnectionScreenController:
    def __init__(self, server, main_controller):
        self.server = server
        self._view = ConnectionScreenView(
            controller=self,
            main_controller=main_controller
        )
        self._init_view()

    def get_view(self):
        return self._view

    def _init_view(self):
        self._view.host.text = self.server.host
        self._view.port.text = str(self.server.port)

    def _check_server(self, *args):
        new_state = args[0]
        if self.server.is_running() and new_state == Server.CONNECTED:
            self._view.connected()

            # since server is created There is a possibility to start it.
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                loop.create_task(self.server.start_server())
        elif not self.server.is_running() and new_state == Server.DISCONNECTED:
            self._view.disconnected()

    async def change_state(self, new_state: str, host: Optional[str] = None, port: Optional[int] = None):
        if new_state == Server.CONNECTED:
            self.server.host = host
            self.server.port = port

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            if new_state == Server.CONNECTED:
                task = loop.create_task(self.server.create_server())
            else:
                task = loop.create_task(self.server.stop_server())
            task.add_done_callback(partial(self._check_server, new_state))

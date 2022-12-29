import asyncio

from src.entrypoints.server.views.connection_screen.connection_screen import \
    ConnectionScreenView


class ConnectionScreenController:
    def __init__(self, server, messagebus):
        self.server = server
        self.messagebus = messagebus
        self._view = ConnectionScreenView(
            controller=self
        )
        self._init_view()

    def get_view(self):
        return self._view

    def _init_view(self):
        self._view.host.text = self.server.host
        self._view.port.text = str(self.server.port)

    def connect(self, host: str, port: int):
        self.server.host = host
        self.server.port = port

        async def start_server():
            await self.server.start_server()

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(start_server())

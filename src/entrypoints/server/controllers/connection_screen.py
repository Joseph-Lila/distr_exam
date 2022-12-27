from src.entrypoints.server.views.connection_screen.connection_screen import \
    ConnectionScreenView


class ConnectionScreenController:
    def __init__(self, server, messagebus):
        self.server = server
        self.messagebus = messagebus
        self._view = ConnectionScreenView(
            controller=self
        )

    def get_view(self):
        return self._view

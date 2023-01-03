from src.entrypoints.client.views.parent_screen.parent_screen import ParentScreenView


class ParentScreenController:
    def __init__(self, server, *args, **kwargs):
        self.server = server
        self._view = ParentScreenView(
            controller=self
        )

    def get_view(self):
        return self._view

    def set_connected_state(self):
        self._view.set_connected_state()

    def set_disconnected_state(self):
        self._view.set_disconnected_state()

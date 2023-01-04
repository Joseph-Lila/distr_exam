from src.entrypoints.client.views.parent_screen.parent_screen import ParentScreenView


class ParentScreenController:
    def __init__(self, client, *args, **kwargs):
        self.client = client
        self._view = ParentScreenView(
            controller=self
        )

    def get_view(self):
        return self._view

    def set_connected_state(self):
        self._view.set_connected_state()

    def set_disconnected_state(self):
        self._view.set_disconnected_state()

    def go_to_connection_screen(self, *args):
        self._view.screen_manager.current = 'connection screen'

    def go_to_data_screen(self, *args):
        self._view.screen_manager.current = 'data screen'

    def go_to_pandas_screen(self, *args):
        self._view.screen_manager.current = 'pandas screen'

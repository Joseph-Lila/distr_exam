from src.entrypoints.client.views.pandas_screen.pandas_screen import PandasScreenView


class PandasScreenController:
    def __init__(self, client, main_controller):
        self.client = client
        self._view = PandasScreenView(
            controller=self,
            main_controller=main_controller
        )

    def get_view(self):
        return self._view

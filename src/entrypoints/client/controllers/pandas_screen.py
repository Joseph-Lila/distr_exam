from src.domain.commands import SendDbDataToServer
from src.domain.utilities import send_message
from src.entrypoints.client.controllers.data_screen import use_loop
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

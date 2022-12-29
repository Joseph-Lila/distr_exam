from src.config import get_tcp_ip_credits
from src.domain.utilities import Server
from src.entrypoints.server.controllers.connection_screen import \
    ConnectionScreenController
from src.entrypoints.server.controllers.parent_screen import \
    ParentScreenController

SCREENS = {
    "connection screen": ConnectionScreenController,
    "parent screen": ParentScreenController,
}


class ScreenGenerator:
    def __init__(self, screens=SCREENS):
        self.screens = screens
        self.server = Server(*get_tcp_ip_credits())
        self._parent_screen_name = 'parent screen'

    def build_app_view(self):
        parent_view = self._generate_view(self._parent_screen_name)
        for key in self.screens.keys():
            if key != self._parent_screen_name:
                parent_view.screen_manager.add_widget(self._generate_view(key, parent_view.controller))
        return parent_view

    def _generate_view(self, key, main_controller=None):
        controller = self.screens[key](self.server, main_controller)
        view = controller.get_view()
        view.name = key
        return view

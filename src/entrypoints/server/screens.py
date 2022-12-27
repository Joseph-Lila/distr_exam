from src.adapters.tcp_ip.domain.models import Server
from src.bootstrap import bootstrap
from src.config import get_tcp_ip_credits
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
        self.messagebus = bootstrap()
        self._parent_screen_name = 'parent screen'

    def build_app_view(self):
        parent_view = self._generate_view(self._parent_screen_name)
        for key in self.screens.keys():
            if key != self._parent_screen_name:
                parent_view.screen_manager.add_widget(self._generate_view(key))
        return parent_view

    def _generate_view(self, key):
        controller = self.screens[key](self.server, self.messagebus)
        view = controller.get_view()
        view.name = key
        return view

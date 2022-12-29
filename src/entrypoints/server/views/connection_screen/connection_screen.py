from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from src.domain.utilities import Server


class ConnectionScreenView(MDScreen):
    main_controller = ObjectProperty()
    controller = ObjectProperty()

    def connected(self):
        self.connect_btn.text = Server.DISCONNECTED
        self.main_controller.set_connected_state()

    def disconnected(self):
        self.connect_btn.text = Server.CONNECTED
        self.main_controller.set_disconnected_state()

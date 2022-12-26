from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

import config
from domain import events


class ConnectionScreenView(MDScreen):
    """ View for connection """

    controller = ObjectProperty()

    def on_kv_post(self, base_widget):
        host, port = config.get_tcp_ip_credits()
        self.host.text, self.port.text = str(host), str(port)

    def process_event(self, event: events.Event):
        print(event)

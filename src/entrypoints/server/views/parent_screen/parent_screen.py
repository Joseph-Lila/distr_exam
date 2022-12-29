from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class ParentScreenView(MDScreen):
    controller = ObjectProperty()

    def set_connected_state(self):
        MDApp.get_running_app().theme_cls.primary_palette = 'Purple'
        self.app_bar.icon_color = [0, 1, 0, 1]

    def set_disconnected_state(self):
        MDApp.get_running_app().theme_cls.primary_palette = 'BlueGray'
        self.app_bar.icon_color = [1, 0, 0, 1]
from kivy.uix.screenmanager import ScreenManager

from client.controllers.connection_screen import ConnectionScreenController


SCREENS = {
    "connection_screen": {
        "controller": ConnectionScreenController
    },
}


def get_main_view():
    screen_manager = ScreenManager()
    for key in SCREENS.keys():
        screen_manager.add_widget(generate_view(key))
    return screen_manager


def generate_view(key):
    controller = SCREENS[key]['controller']()
    view = controller.get_screen()
    view.name = key
    return view

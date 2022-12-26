from client.views.connection_screen.connection_screen import ConnectionScreenView
from domain import commands
from kivy.app import App


class ConnectionScreenController:
    def __init__(self):
        self.view = ConnectionScreenView(controller=self)

    def get_screen(self):
        return self.view

    async def process_command(self, cmd: commands.Command):
        bus = App.get_running_app().bus
        event = await bus.handle_command(cmd)
        self.view.process_event(event)

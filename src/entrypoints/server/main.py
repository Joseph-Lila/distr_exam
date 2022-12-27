from kivymd.app import MDApp

from src.entrypoints.server.screens import ScreenGenerator


class ServerApp(MDApp):
    title = 'Server'

    def build(self):
        self.load_all_kv_files(self.directory)
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    ServerApp().run()

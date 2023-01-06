import asyncio

from kivymd.app import MDApp

from src.entrypoints.server.screens import ScreenGenerator


class ServerApp(MDApp):
    title = 'Server'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(ServerApp().async_run(async_lib='asyncio'))

import asyncio

from kivymd.app import MDApp
import asynckivy as ak
import bootstrap
from client.screens import get_main_view


class ClientApp(MDApp):
    title = "Client"

    async def main(self):
        self.bus = bootstrap.bootstrap()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.bus = None
        ak.start(self.main())

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.material_style = "M3"
        return get_main_view()


if __name__ == "__main__":
    ClientApp().run()

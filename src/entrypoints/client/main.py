# import asyncio
#
# from src.domain.commands import GetMusicFavors
# from src.config import get_tcp_ip_credits
# from src.domain.utilities import Client, send_message, get_message
#
#
# async def main():
#     client = Client(*get_tcp_ip_credits())
#     await client.connect()
#     await send_message(GetMusicFavors(), client.writer)
#     message = await get_message(client.reader)
#     print(message)
#     await client.disconnect()
#
# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio

from kivymd.app import MDApp
from src.entrypoints.client.screens import ScreenGenerator


class ServerApp(MDApp):
    title = 'Client'

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

import asyncio

from src.domain.commands import GetMusicFavors
from src.config import get_tcp_ip_credits
from src.domain.utilities import Client, send_message, get_message


async def main():
    client = Client(*get_tcp_ip_credits())
    await client.connect()
    await send_message(GetMusicFavors(), client.writer)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

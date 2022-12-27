import asyncio

from src.adapters.tcp_ip.domain.commands import SayHi
from src.adapters.tcp_ip.domain.models import Client
from src.config import get_tcp_ip_credits


async def main():
    client = Client(*get_tcp_ip_credits())
    await client.connect()
    await client.send_message(SayHi())
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

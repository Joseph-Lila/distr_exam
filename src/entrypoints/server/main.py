import asyncio

from src.adapters.tcp_ip.domain.models import Server
from src.config import get_tcp_ip_credits


async def main():
    server = Server(*get_tcp_ip_credits())
    await server.start_server()


if __name__ == "__main__":
    asyncio.run(main())

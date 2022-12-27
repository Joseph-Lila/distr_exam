import asyncio
import struct
from typing import Union
from loguru import logger
from src.adapters.tcp_ip.domain.commands import Command, DisconnectFromTheServer
from src.adapters.tcp_ip.domain.events import Event, ServerIsClosed
from src.adapters.tcp_ip.servise_layer.messages_parser import MessagesParser
from src.config import get_encoding


class Client:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port
        )

    async def disconnect(self):
        await self.send_message(DisconnectFromTheServer())
        self._writer.close()

    async def handle_income_messages(self):
        server_message = None
        while server_message != ServerIsClosed():
            server_message = await self.get_message()
            print(server_message)
        await self.disconnect()

    async def send_message(self, message: Union[Command, Event]):
        str_message = MessagesParser.message2str(message)
        self._writer.write(struct.pack('<L', len(str_message)))
        self._writer.write(str_message.encode(get_encoding()))
        await self._writer.drain()

    async def get_message(self) -> Union[Command, Event]:
        size, = struct.unpack('<L', await self._reader.readexactly(4))
        message: Union[Command, Event] = \
            MessagesParser.str2message(str((await self._reader.readexactly(size)).decode(get_encoding())))
        return message


class Server:
    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port
        self._server = None

    async def start_server(self):
        self._server = await asyncio.start_server(self.handle_connection, self._host, self._port)
        await self._server.start_serving()
        await self._server.serve_forever()

    async def stop_server(self):
        logger.info("stop_server called")
        await self._server.wait_closed()
        logger.info('Wait closed!')

    @staticmethod
    async def handle_connection(reader, writer):
        while True:
            try:
                size, = struct.unpack('<L', await reader.readexactly(4))
                message: Union[Command, Event] = \
                    MessagesParser.str2message(str((await reader.readexactly(size)).decode(get_encoding())))
            except ConnectionError:
                logger.exception('Lost connection...')
                break
            logger.info(message)
            if message == DisconnectFromTheServer():
                break

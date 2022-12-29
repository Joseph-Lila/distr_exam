import asyncio
import struct
from typing import Union

from loguru import logger

from src.bootstrap import bootstrap
from src.config import get_encoding
from src.domain.commands import Command
from src.domain.events import Event
from src.service_layer.message_parser import MessageParser


bus = bootstrap()


async def send_message(message: Union[Command, Event], writer: asyncio.StreamWriter):
    str_message = MessageParser.message2str(message)
    writer.write(struct.pack('<L', len(str_message)))
    writer.write(str_message.encode(get_encoding()))
    await writer.drain()


async def get_message(reader: asyncio.StreamReader) -> Union[Command, Event]:
    size, = struct.unpack('<L', await reader.readexactly(4))
    message: Union[Command, Event] = \
        MessageParser.str2message(str((await reader.readexactly(size)).decode(get_encoding())))
    return message


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
        self._writer.close()


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
                message = await get_message(reader)
                response = await bus.handle_command(message)
                await send_message(response, writer)
            except ConnectionError:
                logger.exception('Lost connection...')
                break
            logger.info(message)

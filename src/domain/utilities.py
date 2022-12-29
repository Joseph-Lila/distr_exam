import asyncio
import struct
from typing import Union, Optional

from loguru import logger

from src.bootstrap import bootstrap
from src.config import get_encoding
from src.domain.commands import Command
from src.domain.events import Event
from src.service_layer.message_parser import MessageParser


bus = bootstrap()


async def send_message(message: Union[Command, Event], writer: asyncio.StreamWriter):
    if writer:
        str_message = MessageParser.message2str(message)
        writer.write(struct.pack('<L', len(str_message)))
        writer.write(str_message.encode(get_encoding()))
        await writer.drain()


async def get_message(reader: asyncio.StreamReader) -> Optional[Union[Command, Event]]:
    if reader:
        size, = struct.unpack('<L', await reader.readexactly(4))
        message: Union[Command, Event] = \
            MessageParser.str2message(str((await reader.readexactly(size)).decode(get_encoding())))
        return message


class Client:
    def __init__(self, host=None, port=None):
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    async def connect(self):
        if self._host and self._port:
            self._reader, self._writer = await asyncio.open_connection(
                self._host, self._port
            )

    async def disconnect(self):
        if self._writer:
            self._writer.close()


class Server:
    def __init__(self, host=None, port=None):
        super().__init__()
        self._host = host
        self._port = port
        self._server = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    async def start_server(self):
        if self._host and self._port:
            self._server = await asyncio.start_server(self.handle_connection, self._host, self._port)
            await self._server.start_serving()
            await self._server.serve_forever()

    async def is_running(self):
        return self._server.is_serving()

    async def stop_server(self):
        if self._server.is_serving():
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

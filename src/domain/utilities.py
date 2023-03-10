import asyncio
import struct
from typing import Optional, Union

from loguru import logger

from src.bootstrap import bootstrap
from src.config import get_additional_sqlite_connection_str, get_encoding
from src.domain.commands import (AddMusicFavor, Command, GetMusicFavors,
                                 SendDbDataToServer)
from src.domain.events import DbDataIsSentFromServer, Event
from src.service_layer.message_parser import MessageParser
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import \
    AiosqliteUnitOfWork

bus = bootstrap()
additional_bus = bootstrap(uow=AiosqliteUnitOfWork(connection_string=get_additional_sqlite_connection_str()))


async def send_message(message: Union[Command, Event], writer: asyncio.StreamWriter):
    if writer:
        try:
            str_message = MessageParser.message2str(message)
            writer.write(struct.pack('<L', len(str_message)))
            writer.write(str_message.encode(get_encoding()))
            await writer.drain()
        except Exception:
            raise Exception('Connection Lost')


async def get_message(reader: asyncio.StreamReader) -> Optional[Union[Command, Event]]:
    if reader:
        size, = struct.unpack('<L', await reader.readexactly(4))
        message: Union[Command, Event] = \
            MessageParser.str2message(str((await reader.readexactly(size)).decode(get_encoding())))
        return message


class Client:
    CONNECTED = 'Connect'
    DISCONNECTED = 'Disconnect'

    def __init__(self, host=None, port=None):
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None
        self.connected = False

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

    @property
    def reader(self):
        return self._reader

    @property
    def writer(self):
        return self._writer

    async def connect(self):
        if self._host and self._port:
            try:
                self._reader, self._writer = await asyncio.open_connection(
                    self._host, self._port
                )
                self.connected = True
            except Exception as e:
                logger.warning('???????????? ?????? ?????????????? ??????????????????????.')
                self.connected = False

    async def disconnect(self):
        if self._writer:
            self._writer.close()
            self.connected = False

    @staticmethod
    async def fill_additional_db(event: DbDataIsSentFromServer):
        if type(event) == DbDataIsSentFromServer:
            async with additional_bus.uow:
                await additional_bus.uow.music_favors.clear_table()
                await additional_bus.uow.commit()
            for item in event.data:
                await additional_bus.handle_command(AddMusicFavor(item))

    @staticmethod
    async def share_additional_db():
        records = await additional_bus.handle_command(GetMusicFavors())
        return records


class Server:
    CONNECTED = 'Connect'
    DISCONNECTED = 'Disconnect'

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

    async def create_server(self):
        if self._host and self._port:
            self._server = await asyncio.start_server(self.handle_connection, self._host, self._port)

    async def start_server(self):
        if self._server:
            await self._server.start_serving()
            await self._server.serve_forever()

    def is_running(self):
        return self._server.is_serving()

    async def stop_server(self):
        if self._server.is_serving():
            self._server.close()
            await self._server.wait_closed()

    @staticmethod
    async def handle_connection(reader, writer):
        while True:
            try:
                message = await get_message(reader)
                response = await bus.handle_command(message)
                await send_message(response, writer)
            except Exception:
                break
            logger.info(message)

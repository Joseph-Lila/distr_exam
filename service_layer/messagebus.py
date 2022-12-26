from typing import Callable, Type, Dict

from domain import commands, events
from service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork
from loguru import logger


class MessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork,
            command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.uow = uow
        self.command_handlers = command_handlers

    async def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            await handler(command)
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise

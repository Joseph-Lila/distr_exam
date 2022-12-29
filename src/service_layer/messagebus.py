from typing import Callable, Dict, Type

from loguru import logger

from src.domain import commands
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


class MessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork,
            command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.uow = uow
        self.command_handlers = command_handlers

    async def handle_command(self, command: commands.Command):
        logger.debug(f"handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            return await handler(command)
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise

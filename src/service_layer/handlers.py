from typing import Callable, Dict, Type

from src.domain import commands, events
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


async def add_music_favor(
        cmd: commands.AddRecord,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.music_favors.create(cmd.new_item)
        await uow.commit()
    return events.RecordIsAdded(cmd.new_item)


async def get_data(
        cmd: commands.GetData,
        uow: AbstractUnitOfWork,
):
    async with uow:
        records = await uow.music_favors.get_all()
    return events.DataIsGiven(records)


async def make_request(
        cmd: commands.MakeRequest,
        uow: AbstractUnitOfWork,
):
    async with uow:
        records = await uow.music_favors.get_all()
    records = [record for record in records if cmd.function(record)]
    return events.MadeRequest(records)


COMMAND_HANDLERS = {
    commands.GetData: get_data,
    commands.MakeRequest: make_request,
    commands.AddRecord: add_music_favor,
}  # type: Dict[Type[commands.Command], Callable]

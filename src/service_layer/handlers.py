from typing import Callable, Dict, Type

from src.domain import commands, events
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


async def add_music_favor(
        cmd: commands.AddMusicFavor,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.music_favors.create(cmd.new_item)
        await uow.commit()
    return events.RecordIsAdded(cmd.new_item)


async def get_data(
        cmd: commands.GetMusicFavors,
        uow: AbstractUnitOfWork,
):
    async with uow:
        records = await uow.music_favors.get_all()
    return events.DataIsGiven(records)


async def make_request(
        cmd: commands.GetMusicFavorsBySubstring,
        uow: AbstractUnitOfWork,
):
    async with uow:
        records = await uow.music_favors.get_all()
    records = [record for record in records if cmd.substring in record.group_name]
    return events.MadeRequest(records)


async def send_db_data_to_server(
        cmd: commands.SendDbDataToServer,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.music_favors.clear_table()
        await uow.commit()
        for item in cmd.data:
            await uow.music_favors.create(item)
        await uow.commit()
    return events.DbDataIsSentToServer()


async def get_db_data_from_server(
        cmd: commands.GetDbDataFromServer,
        uow: AbstractUnitOfWork,
):
    async with uow:
        records = await uow.music_favors.get_all()
    return events.DbDataIsSentFromServer(records)


COMMAND_HANDLERS = {
    commands.GetMusicFavors: get_data,
    commands.GetMusicFavorsBySubstring: make_request,
    commands.AddMusicFavor: add_music_favor,
    commands.SendDbDataToServer: send_db_data_to_server,
    commands.GetDbDataFromServer: get_db_data_from_server,
}  # type: Dict[Type[commands.Command], Callable]

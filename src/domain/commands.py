from dataclasses import dataclass
from typing import List

from src.domain.models import MusicFavor


@dataclass
class Command:
    pass


@dataclass
class AddMusicFavor(Command):
    new_item: MusicFavor


@dataclass
class GetMusicFavors(Command):
    pass


@dataclass
class GetMusicFavorsBySubstring(Command):
    substring: str


@dataclass
class SendDbDataToServer(Command):
    data: List[MusicFavor]


@dataclass
class GetDbDataFromServer(Command):
    pass


class_dict = {
    'Command': Command,
    'AddMusicFavor': AddMusicFavor,
    'GetMusicFavors': GetMusicFavors,
    'GetMusicFavorsBySubstring': GetMusicFavorsBySubstring,
    'SendDbDataToServer': SendDbDataToServer,
    'GetDbDataFromServer': GetDbDataFromServer,
}

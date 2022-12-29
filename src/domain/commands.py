from dataclasses import dataclass

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


class_dict = {
    'Command': Command,
    'AddMusicFavor': AddMusicFavor,
    'GetMusicFavors': GetMusicFavors,
    'GetMusicFavorsBySubstring': GetMusicFavorsBySubstring,
}

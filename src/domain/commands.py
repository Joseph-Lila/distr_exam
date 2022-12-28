from dataclasses import dataclass

from src.domain.models import BaseEntity


class Command:
    pass


@dataclass
class AddMusicFavor(Command):
    new_item: BaseEntity


@dataclass
class GetMusicFavors(Command):
    pass


@dataclass
class GetMusicFavorsBySubstring(Command):
    substring: str

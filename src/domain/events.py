from dataclasses import dataclass
from typing import List

from src.domain.models import MusicFavor


@dataclass
class Event:
    pass


@dataclass
class RecordIsAdded(Event):
    new_item: MusicFavor


@dataclass
class DataIsGiven(Event):
    data: List[MusicFavor]


@dataclass
class MadeRequest(Event):
    data: List[MusicFavor]


@dataclass
class DbDataIsSentToServer(Event):
    pass


@dataclass
class DbDataIsSentFromServer(Event):
    data: List[MusicFavor]


class_dict = {
    'Event': Event,
    'RecordIsAdded': RecordIsAdded,
    'DataIsGiven': DataIsGiven,
    'MadeRequest': MadeRequest,
    'DbDataIsSentToServer': DbDataIsSentToServer,
    'DbDataIsSentFromServer': DbDataIsSentFromServer,
}

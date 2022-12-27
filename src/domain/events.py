from dataclasses import dataclass
from typing import List

from src.domain.models import BaseEntity


class Event:
    pass


@dataclass
class RecordIsAdded(Event):
    new_item: BaseEntity


@dataclass
class DataIsGiven(Event):
    data: List[BaseEntity]


@dataclass
class MadeRequest(Event):
    data: List[BaseEntity]

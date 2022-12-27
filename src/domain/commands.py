from dataclasses import dataclass
from typing import Callable

from src.domain.models import BaseEntity


class Command:
    pass


@dataclass
class AddRecord(Command):
    new_item: BaseEntity


@dataclass
class GetData(Command):
    pass


@dataclass
class MakeRequest(Command):
    function: Callable

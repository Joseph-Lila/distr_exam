""" Module domain.models """

from dataclasses import dataclass


@dataclass
class BaseEntity:
    """ BaseEntity implementation """
    item_id: int = 0


@dataclass
class Cat(BaseEntity):
    """ Example class """
    nick: str = 'Unknown'


@dataclass
class MusicFavor(BaseEntity):
    group_name: str = 'Unknown'
    country: str = 'Unknown'
    mentor_surname: str = 'Unknown'
    written_disks_quantity: int = 0
    total_disks_quantity: int = 0

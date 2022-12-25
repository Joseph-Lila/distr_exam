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

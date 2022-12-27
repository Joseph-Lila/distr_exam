from dataclasses import dataclass


@dataclass
class Event:
    pass


@dataclass
class ServerIsClosed(Event):
    pass


class_dict = {
    'Event': Event,
    'ServerIsClosed': ServerIsClosed,
}

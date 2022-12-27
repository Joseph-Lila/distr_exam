from dataclasses import dataclass


@dataclass
class Command:
    pass


@dataclass
class SayHi(Command):
    pass


@dataclass
class DisconnectFromTheServer(Command):
    pass


class_dict = {
    'Command': Command,
    'SayHi': SayHi,
    'DisconnectFromTheServer': DisconnectFromTheServer,
}

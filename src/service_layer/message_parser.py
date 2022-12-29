import dataclass_factory
import json
from typing import Union
from dataclasses import asdict
from src.domain import commands, events

class_dict = {}
class_dict.update(commands.class_dict)
class_dict.update(events.class_dict)


class MessageParser:

    @staticmethod
    def message2str(message: Union[commands.Command, events.Event]):
        dict_message = asdict(message)
        dict_message['type'] = type(message).__name__
        str_message = json.dumps(dict_message)
        return str_message

    @staticmethod
    def str2message(str_message: str) -> Union[commands.Command, events.Event]:
        dict_message: dict = json.loads(str_message)
        type_name = dict_message.pop('type')
        message_type = class_dict[type_name]
        factory = dataclass_factory.Factory()
        message = factory.load(dict_message, message_type)
        return message

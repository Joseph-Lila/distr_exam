from src.adapters.tcp_ip.domain.commands import DisconnectFromTheServer
from src.adapters.tcp_ip.domain.events import ServerIsClosed
from src.adapters.tcp_ip.servise_layer.messages_parser import MessagesParser


def test_message2str_command():
    message = DisconnectFromTheServer()
    expected = '{"type": "DisconnectFromTheServer"}'
    outcome = MessagesParser.message2str(message)
    assert expected == outcome


def test_message2str_event():
    message = ServerIsClosed()
    expected = '{"type": "ServerIsClosed"}'
    outcome = MessagesParser.message2str(message)
    assert expected == outcome


def test_str2message_command():
    str_message = '{"type": "DisconnectFromTheServer"}'
    expected = DisconnectFromTheServer()
    outcome = MessagesParser.str2message(str_message)
    assert expected == outcome


def test_str2message_event():
    str_message = '{"type": "ServerIsClosed"}'
    expected = ServerIsClosed()
    outcome = MessagesParser.str2message(str_message)
    assert expected == outcome

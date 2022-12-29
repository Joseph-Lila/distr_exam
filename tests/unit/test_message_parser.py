from src.domain.commands import AddMusicFavor, GetMusicFavors, GetMusicFavorsBySubstring
from src.domain.events import RecordIsAdded, DataIsGiven, MadeRequest
from src.domain.models import MusicFavor
from src.service_layer.message_parser import MessageParser


def test_message2str_add_music_favor_command():
    new_item = MusicFavor()
    message = AddMusicFavor(new_item=new_item)
    expected = '{"new_item": {"item_id": 0, "group_name": "Unknown", ' \
               '"country": "Unknown", "mentor_surname": "Unknown", ' \
               '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
               '"type": "AddMusicFavor"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_message2str_get_music_favors_command():
    message = GetMusicFavors()
    expected = '{"type": "GetMusicFavors"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_message2str_get_music_favors_by_substring_command():
    message = GetMusicFavorsBySubstring(substring='GroupName')
    expected = '{"substring": "GroupName", "type": "GetMusicFavorsBySubstring"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_message2str_record_is_added_event():
    new_item = MusicFavor()
    message = RecordIsAdded(new_item)
    expected = '{"new_item": {"item_id": 0, "group_name": "Unknown", ' \
               '"country": "Unknown", "mentor_surname": "Unknown", ' \
               '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
               '"type": "RecordIsAdded"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_message2str_data_is_given_event():
    data = [MusicFavor(item_id=1), MusicFavor(item_id=2)]
    message = DataIsGiven(data)
    expected = '{"data": ' \
               '[{"item_id": 1, "group_name": "Unknown", ' \
               '"country": "Unknown", "mentor_surname": "Unknown", ' \
               '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
               '{"item_id": 2, "group_name": "Unknown", "country": "Unknown", ' \
               '"mentor_surname": "Unknown", "written_disks_quantity": 0, ' \
               '"total_disks_quantity": 0}], "type": "DataIsGiven"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_message2str_made_request_event():
    data = [MusicFavor(item_id=1), MusicFavor(item_id=2)]
    message = MadeRequest(data)
    expected = '{"data": ' \
               '[{"item_id": 1, "group_name": "Unknown", ' \
               '"country": "Unknown", "mentor_surname": "Unknown", ' \
               '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
               '{"item_id": 2, "group_name": "Unknown", "country": "Unknown", ' \
               '"mentor_surname": "Unknown", "written_disks_quantity": 0, ' \
               '"total_disks_quantity": 0}], "type": "MadeRequest"}'
    outcome = MessageParser.message2str(message)
    assert expected == outcome


def test_str2message_add_music_favor_command():
    new_item = MusicFavor()
    expected = AddMusicFavor(new_item=new_item)
    str_message = '{"new_item": {"item_id": 0, "group_name": "Unknown", ' \
                  '"country": "Unknown", "mentor_surname": "Unknown", ' \
                  '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
                  '"type": "AddMusicFavor"}'
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome


def test_str2message_get_music_favors_command():
    expected = GetMusicFavors()
    str_message = '{"type": "GetMusicFavors"}'
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome


def test_str2message_get_music_favors_by_substring_command():
    str_message = '{"substring": "GroupName", "type": "GetMusicFavorsBySubstring"}'
    expected = GetMusicFavorsBySubstring(substring='GroupName')
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome


def test_str2message_record_is_added_event():
    new_item = MusicFavor()
    expected = RecordIsAdded(new_item)
    str_message = '{"new_item": {"item_id": 0, "group_name": "Unknown", ' \
                  '"country": "Unknown", "mentor_surname": "Unknown", ' \
                  '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
                  '"type": "RecordIsAdded"}'
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome


def test_str2message_data_is_given_event():
    data = [MusicFavor(item_id=1), MusicFavor(item_id=2)]
    expected = DataIsGiven(data)
    str_message = '{"data": ' \
                  '[{"item_id": 1, "group_name": "Unknown", ' \
                  '"country": "Unknown", "mentor_surname": "Unknown", ' \
                  '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
                  '{"item_id": 2, "group_name": "Unknown", "country": "Unknown", ' \
                  '"mentor_surname": "Unknown", "written_disks_quantity": 0, ' \
                  '"total_disks_quantity": 0}], "type": "DataIsGiven"}'
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome


def test_str2message_made_request_event():
    data = [MusicFavor(item_id=1), MusicFavor(item_id=2)]
    expected = MadeRequest(data)
    str_message = '{"data": ' \
                  '[{"item_id": 1, "group_name": "Unknown", ' \
                  '"country": "Unknown", "mentor_surname": "Unknown", ' \
                  '"written_disks_quantity": 0, "total_disks_quantity": 0}, ' \
                  '{"item_id": 2, "group_name": "Unknown", "country": "Unknown", ' \
                  '"mentor_surname": "Unknown", "written_disks_quantity": 0, ' \
                  '"total_disks_quantity": 0}], "type": "MadeRequest"}'
    outcome = MessageParser.str2message(str_message)
    assert expected == outcome

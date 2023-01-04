from typing import List

from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
import asynckivy as ak
from dataclasses import astuple

from kivymd.uix.snackbar import Snackbar

from src.domain.models import MusicFavor


class DataScreenView(MDScreen):
    main_controller = ObjectProperty()
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_table = None
        self.add_music_favor_popup_content_cls = None
        self._init_view()

    def on_enter(self, *args):
        ak.start(self.controller.send_get_data_command())

    def _init_view(self):
        ak.start(self._add_data_table())

    async def _add_data_table(self):
        self._data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("ID", dp(20)),
                ("Название группы", dp(35)),
                ("Страна", dp(35)),
                ("Фамилия руководителя", dp(35)),
                ("Количество записанных дисков", dp(25)),
                ("Общий тираж", dp(25)),
            ],
            row_data=[],
            elevation=2,
        )
        self.data_table_cont.add_widget(self._data_table)

    async def record_is_added(self, new_item: MusicFavor):
        new_item_tuple = astuple(new_item)
        self._data_table.row_data.append(new_item_tuple)

    async def data_is_given(self, data: List[MusicFavor]):
        self._data_table.row_data.clear()
        for item in data:
            item_tuple = astuple(item)
            self._data_table.row_data.append(item_tuple)

    def open_add_music_favor_popup(self, *args):
        self.add_music_favor_popup_content_cls = Factory.DialogAddMusicFavor()
        buttons = Factory.OKButton(on_release=self._prepare_person_to_adding)
        MDDialog(
            title='Add person',
            type='custom',
            content_cls=self.add_music_favor_popup_content_cls,
            buttons=[buttons]
        ).open()

    def _prepare_person_to_adding(self, *args):
        music_favor_to_add = MusicFavor(
            group_name=self.add_music_favor_popup_content_cls.group_name.text,
            country=self.add_music_favor_popup_content_cls.country.text,
            mentor_surname=self.add_music_favor_popup_content_cls.mentor_surname.text,
            written_disks_quantity=int(self.add_music_favor_popup_content_cls.written_disks_quantity.text),
            total_disks_quantity=int(self.add_music_favor_popup_content_cls.total_disks_quantity.text)
        )
        ak.start(self.controller.send_add_command(music_favor_to_add))

    def show_lost_connection_snackbar(self):
        self._data_table.row_data = []
        Snackbar(text="Connection Lost...").open()

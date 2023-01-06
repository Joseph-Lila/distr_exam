from dataclasses import astuple
from typing import List

import numpy as np
import pandas as pd
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from src.domain.models import MusicFavor


class PandasScreenView(MDScreen):
    main_controller = ObjectProperty()
    controller = ObjectProperty()

    async def data_is_given(self, data: List[MusicFavor]):
        self.data_table_cont.clear_widgets()
        if not (self.search_mode.current_active_segment and self.search_section.current_active_segment):
            self.show_snackbar('Выберите разрез данных и режим просмотра!')
            return
        search_mode = self.search_mode.current_active_segment.text
        search_section = self.search_section.current_active_segment.text
        df = pd.DataFrame([astuple(item) for item in data],
                          columns=['id', 'название группы', 'страна',
                                   'фамилия руководителя',
                                   'количество записанных дисков',
                                   'общий тираж дисков']
                          )
        pivot = pd.pivot_table(
            df,
            values='количество записанных дисков' if search_section == 'Кол-во дисков' else 'общий тираж дисков',
            index=['название группы'] if search_mode == 'Старт' or search_mode == 'Итоги' else ['страна'],
            columns=['страна'] if search_mode == 'Старт' or search_mode == 'Итоги' else ['название группы'],
            aggfunc=np.sum,
            fill_value=0,
            margins=True if search_mode == 'Итоги' or search_mode == 'Поменять местами' else False,
            margins_name='Total',
        )

        cols = ['Название группы'] + pivot.columns.values.tolist() if search_mode == 'Старт' or search_mode == 'Итоги' else ['Страна'] + pivot.columns.values.tolist()
        values = pivot.values.tolist()
        indexes = pivot.index.values.tolist()
        rows = [[indexes[i]] + lst for i, lst in enumerate(values)]

        data_table = MDDataTable(
            use_pagination=True,
            column_data=[(col, dp(30)) for col in cols],
            row_data=rows
        )

        self.data_table_cont.add_widget(data_table)

    @staticmethod
    def show_snackbar(text):
        Snackbar(text=text, snackbar_animation_dir='Top').open()

    @staticmethod
    def show_lost_connection_snackbar():
        Snackbar(text="Connection Lost...").open()

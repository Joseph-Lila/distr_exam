from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class PandasScreenView(MDScreen):
    main_controller = ObjectProperty()
    controller = ObjectProperty()

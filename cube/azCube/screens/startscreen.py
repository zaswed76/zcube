from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton




class StartScreen(Screen):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
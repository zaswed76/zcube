from kivy.uix.screenmanager import Screen


class TrainingScreen(Screen):
    def __init__(self, stored_data, **kw):
        super().__init__(**kw)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class ListItem(BoxLayout):
    def __init__(self, text, field=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.option_label.text = text
        if field is not None:
            self.ids.option_field.text = str(field)



class SettingsView(Screen):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.options = {}
        self.store = store
        items = ["parts"]
        for i in items:
            self.options[i] = ListItem(str(i), self.store.get("ui").get("parts"))
            self.settings_box.add_widget(self.options[i])
        self.settings_box.add_widget(Label())
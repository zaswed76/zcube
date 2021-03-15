from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel


class ListItem(BoxLayout):
    def __init__(self, text, field=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.option_label.text = text
        if field is not None:
            self.ids.option_field.text = str(field)

class ListItemButton(BoxLayout):
    def __init__(self, text="", _icon="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = 1, None
        self.height = 50
        self.padding = (20, 0, 20, 0)
        lb = MDLabel(text=text)
        self.btn = MDRaisedButton(on_press=MDApp.get_running_app().color_pick)
        self.btn.name = "bg_view_color"
        self.add_widget(lb)
        self.add_widget(self.btn)

    def set_color(self, color):
        self.btn.md_bg_color = color




class SettingsView(Screen):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.options = {}
        self.store = store
        items = ["parts"]

        self.options["parts"] = ListItem(str("parts"), self.store.get("ui").get("parts"))
        self.settings_box.add_widget(self.options["parts"])


        self.options["color"] = ListItemButton("фон", "")
        self.options["color"].set_color(self.store.get("ui").get("bg_view_color", (1, 1, 1, 1)))
        self.settings_box.add_widget(self.options["color"])

        self.settings_box.add_widget(Label())
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton


class ColorPickerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint = 0.9, 0.9
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        box = BoxLayout()
        box.orientation = "vertical"
        self.add_widget(box)

        self.pick_btn = MDRaisedButton(on_press=self.press_ok)
        self.pick_btn.size_hint = 1, 0.1
        self.pick_btn.text = "пример"



        self.app = MDApp.get_running_app()
        self.current_color = None
        self.clr_picker = ColorPicker()
        self.clr_picker.bind(color=self.on_color)

        okbtn = MDRaisedButton(on_press=self.press_ok)
        okbtn.text = "принять"

        box.add_widget(self.pick_btn)
        box.add_widget(self.clr_picker)

        box.add_widget(okbtn)


    def press_ok(self, v):

        self.app.screen_manager.current = "settings_view"
        self.app.settings_view.options["color"].set_color(self.current_color)
        self.app.view .set_color(self.current_color)
        self.pick_btn.md_bg_color = self.current_color

    def on_color(self, instance, value):
        self.current_color = value
        self.pick_btn.md_bg_color = self.current_color



import itertools

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.list import BaseListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.textfield import MDTextField


class NumButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.app.number_generator.current_simbol == "<":
                self.app.number_generator.clean_text_field()
        super().on_touch_down(touch)


class NavigationDrawer(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_status(self, *_):
        if self.state == "close" and self.open_progress == 0.0:
            App.get_running_app().number_generator.set_options()
            # Window.release_all_keyboards()

        super().update_status(*_)


class ItemList(BaseListItem):
    def __init__(self, option, lb_text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = 1, None
        self.height = 70

        self.lb = MDLabel()
        # self.lb.height = 70
        self.lb.halign = "left"
        self.lb.text = lb_text
        self.lb.pos_hint = {"y": -0.1, "x": 0.05}

        self.option_field = MDTextField()
        self.option_field.text = str(option)
        # self.option_field.height = 70
        self.option_field.size_hint = 0.15, None
        self.option_field.pos_hint = {"y": 0.00, "center_x": .65}

        self.add_widget(self.lb)
        self.add_widget(self.option_field)


class ContentNavigationDrawer(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView()
        self.add_widget(self.scroll)
        self.mdlist = MDList()
        self.scroll.add_widget(self.mdlist)


class NumberGenerator(Screen):
    nav_drawer = ObjectProperty()
    content_navigation = ObjectProperty()
    generator_label = ObjectProperty()
    generator_field = ObjectProperty()
    bottom_scroll = ObjectProperty()

    def __init__(self, random_generator_core, stored_data, **kw):
        super().__init__(**kw)
        self.stored_data = stored_data
        self._options = {}
        self._options["start"] = stored_data.get("generator")["start"]
        self._options["end"] = stored_data.get("generator")["end"]
        self._options["count"] = stored_data.get("generator")["count"]
        self._options["sep"] = stored_data.get("generator")["sep"]
        self._options["font_size"] = stored_data.get("generator")["font_size"]
        self.tex_field = []
        self.current_random = None
        self.tex_field_blocked = False
        self.start = False
        self.current_simbol = None
        self._init_option()
        self._init_num_grid()
        self.update_font_fields()


        self.random_generator_core = random_generator_core

    def update_font_fields(self):
        self.generator_label.font_size = self._options["font_size"]
        self.generator_field.font_size = self._options["font_size"]

    def _init_num_grid(self):
        names = ('1', '2', '3', '4', '5', '6', '7', '8', '9', "<", '0', "?")
        for n in names:


            btn = NumButton(text=n, on_press=self.pres_num)
            if n in ["<", "?"]:
                btn.background_color = 0, .7, .7, .8
            self.num_grid.add_widget(btn)

    def pres_num(self, widget):

        self.current_simbol = widget.text

        if self.current_simbol == "<":
            if self.tex_field:
                self.tex_field.pop()
                self.ids.generator_label.text = ""
                self.ids.generator_label.line_color_normal = 0.7, .7, .7, .4
        elif self.current_simbol == "?":
            self.ids.generator_label.text = self.label_random_text
        elif not self.tex_field_blocked:
            self.bottom_scroll.scroll_y = 1
            self.tex_field.append(self.current_simbol)


            if len(self.tex_field) > 0:
                self.start = True
                self.ids.generator_label.text = ""
        self.ids.generator_field.text = "".join(self.tex_field)
        self.on_error(self.current_simbol)

    def clean_text_field(self):
        self.tex_field.clear()
        self.ids.generator_field.text = ""

    def on_finish(self):
        if len(self.ids.generator_field.text) >= len(self.current_random):
            self.tex_field_blocked = True
        else:
            self.tex_field_blocked = False


    def on_error(self, text):
        if self.current_random:
            cursor = len(self.ids.generator_field.text)
            # ошибка
            if self.ids.generator_field.text != "".join(self.current_random[:cursor]):
                self.ids.generator_field.line_color_normal = 1, 0, 0, 1
                self.tex_field_blocked = True
            # финиш
            elif len(self.ids.generator_field.text) >= len(self.current_random):
                self.tex_field_blocked = True
                self.ids.generator_label.text = self.label_random_text
                self.ids.generator_label.line_color_normal = 0, .4, 0.2, 1
            # верно
            elif not len(self.ids.generator_field.text):
                self.tex_field_blocked = False
                self.ids.generator_field.line_color_normal = 0.7, .7, .7, .4
                self.ids.generator_label.text = self.label_random_text
            else:
                self.tex_field_blocked = False
                self.ids.generator_field.line_color_normal = 0.7, .7, .7, .4



    def set_options(self):
        for k, item in self.options.items():
            self._options[k] = item.option_field.text
        self.update_font_fields()

    def _init_option(self):
        options_list = [("начало", "start"), ("конец", "end"), ("колличество", "count"),
                        ("разделитель", "sep"), ("размер шрифта", "font_size")]
        self.options = {}

        for name, opt in options_list:
            v = self._options[opt]
            if v.endswith("sp"):
                v = v.replace('sp', '')
            self.options[opt] = ItemList(v, lb_text=name)
            self.content_navigation.mdlist.add_widget(self.options[opt])
        # self.content_navigation.mdlist.add_widget(Label())

    def generate(self):
            if self.valid_value(self._options["start"],  self._options["end"], self._options["count"]):
                _current_random = self.random_generator_core.not_repeat(int(self._options["start"]),
                                                          int(self._options["end"]),
                                                          int(self._options["count"]))
                self.current_random = list(itertools.chain(*[list(x) for x in _current_random]))
                self.label_random_text = self._options["sep"].join(_current_random)
                self.ids.generator_label.text = self.label_random_text
                self.ids.generator_label.line_color_normal = 0.7, .7, .7, .4
            self.clean_text_field()

    def valid_value(self, start, end, count):
        if all([start, end, count]) and count != "0" and end != "0" and int(end) > int(start):
            return True


import itertools
from functools import partial

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import BaseListItem, MDList, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivy import utils
from kivy.clock import Clock

RoyalBlueColor = utils.get_color_from_hex("#4169E1")
LightSeaGreenColor = utils.get_color_from_hex("#20B2AA")
ForestGreenColor = utils.get_color_from_hex("#228B22")
LightSlateGreyColor = utils.get_color_from_hex("#778899")


class NumButton(Button):
    def __init__(self, normal_color=None, checked_color=None, **kwargs):
        super().__init__(**kwargs)

        self.checked_color = checked_color
        self.normal_color = normal_color
        self.background_color = self.normal_color

        self.app = App.get_running_app()
        self.checkable = False
        self._checked = False

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, checked):
        if checked:
            self.background_color = self.checked_color
        else:
            self.background_color = self.normal_color
        self._checked = checked


    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.app.number_generator.current_simbol == "<":
                self.app.number_generator.clean_text_field()
        super().on_touch_down(touch)

    def on_press(self, *args):
        if self.checkable:
            self.checked = not self.checked






class NavigationDrawer(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_status(self, *_):
        if self.state == "close" and self.open_progress == 0.0:
            App.get_running_app().number_generator.set_options()
        super().update_status(*_)


class ItemFieldList(BoxLayout):
    def __init__(self, name, option, field_label_text, **kwargs):
        super().__init__(**kwargs)

        self.item_field = self.ids.item_field
        self.item_field_label= self.ids.item_field_label
        self.item_field.name = name
        self.ids.item_field_label.text = field_label_text
        self.item_field.text = option


class ContentNavigationDrawer(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def close_driver(self, v):
        self.parent.set_state("close")

class NumberGenerator(Screen):
    nav_drawer = ObjectProperty()
    content_navigation = ObjectProperty()
    generator_label = ObjectProperty()
    generator_field = ObjectProperty()
    bottom_scroll = ObjectProperty()
    box_content = ObjectProperty()

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
        self.current_random = []
        self.current_random_memory = stored_data.get("generator")["current_random"]
        self.tex_field_blocked = False
        self.tex_field_blocked_blocked = False
        self.label_random_text = ''
        self.start = False
        self.current_simbol = None

        self._init_option()
        self._init_num_grid()
        # self.update_font_fields()


        self.random_generator_core = random_generator_core

    def update_font_fields(self):
        self.generator_label.font_size = self._options["font_size"]
        self.generator_field.font_size = self._options["font_size"]

    def _init_num_grid(self):
        names = ('1', '2', '3', "M+", '4', '5', '6', "M", '7','8', '9', "B", "<", '0', "?", "C")
        for n in names:
            if n == "B":
                btn = NumButton(normal_color=RoyalBlueColor,
                                checked_color=ForestGreenColor,
                                text=n, on_press=self.pres_num)
                btn.checkable = True
            elif n in ["<", "?", "C"]:
                btn = NumButton(normal_color=LightSeaGreenColor,
                                text=n, on_press=self.pres_num)
            elif n in ("M", "M+"):
                btn = NumButton(normal_color=RoyalBlueColor,
                                text=n, on_press=self.pres_num)
            else:
                btn = NumButton(normal_color=LightSlateGreyColor,
                                text=n, on_press=self.pres_num)
            self.num_grid.add_widget(btn)

    def pres_num(self, widget):

        self.current_simbol = widget.text

        if self.current_simbol == "<":
            if self.tex_field:
                self.tex_field.pop()
                if not self.tex_field_blocked_blocked:
                    self.ids.generator_label.text = ""
                self.ids.generator_label.line_color_normal = 0.7, .7, .7, .4
        elif self.current_simbol == "?":
            if self.label_random_text:
                self.ids.generator_label.text = self.label_random_text
        elif self.current_simbol == "M+":
            self.current_random_memory = self._current_random_origin.copy()
        elif self.current_simbol == "M":
            self._current_random_origin = self.current_random_memory.copy()
            self.set_generator_label(self._current_random_origin)

        elif self.current_simbol == "B":
            self.tex_field_blocked_blocked = not self.tex_field_blocked_blocked
            if self.tex_field_blocked_blocked:
                self.ids.generator_label.text = self.label_random_text
            else:
                self.ids.generator_label.text = ""
        elif self.current_simbol == "C":
            self.clean_text_field()
        elif not self.tex_field_blocked:
            self.bottom_scroll.scroll_y = 1
            self.tex_field.append(self.current_simbol)


            if len(self.tex_field) > 0:
                self.start = True
                if not self.tex_field_blocked_blocked:
                    self.ids.generator_label.text = ""
        self.ids.generator_field.text = "".join(self.tex_field)
        self.on_error(self.current_simbol)

    def clean_text_field(self):
        self.tex_field.clear()
        self.ids.generator_field.text = ""
        self.ids.generator_label.line_color_normal = 0.7, .7, .7, .4

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
                self.ids.generator_label.line_color_normal = 0, .7, 0.1, 1
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
            self._options[k] = item.item_field.text
        self.update_font_fields()

    def _init_option(self):
        options_list = [("начало", "start", "int"), ("конец", "end", "int"), ("колличество", "count", "int"),
                        ("разделитель", "sep", None), ("размер шрифта", "font_size", "int")]
        self.options = {}

        for name, opt, *flag in options_list:
            filter = flag[0]
            v = self._options[opt]
            if v.endswith("sp"):
                v = v.replace('sp', '')
            self.options[opt] = ItemFieldList(opt, v, name)
            self.options[opt].item_field.bind(text=self.on_text)
            if filter:
                self.options[opt].input_filter = filter
            self.box_content.add_widget(self.options[opt])
        strech = MDLabel()
        # strech.text = "sdgfaerg \nsdefawef"
        strech.size_hint = 1, 0.1
        self.box_content.add_widget(strech)

        close_box = FloatLayout()
        close_box.size_hint = 1, 0.1
        self.box_content.add_widget(close_box)
        close = MDIconButton(on_press=self.content_navigation.close_driver)
        close.pos_hint = {"x": 0.8, "bottom": 0.3}
        close.icon = "close"
        close.user_font_size = "18sp"
        close_box.add_widget(close)


    def on_text(self, *args):
        self.valid_text(*args)

    def valid_text(self, opt, val):
        print(opt.name, val)
        start = self.options["start"].item_field.text
        end = self.options["end"].item_field.text
        count = self.options["count"].item_field.text
        if opt.name == "end":

            if not val or int(val) <= int(start):
                self.options["end"].item_field_label.text_color = 1, 0,0,1
                self.options["end"].item_field_label.text = "конец" + " > начало"
            else:
                self.options["end"].item_field_label.text_color = 0.7, 0.7, 0.7, 1
                self.options["end"].item_field_label.text = "конец"
                self.options["start"].item_field_label.text_color = 0.7, 0.7, 0.7, 1
                self.options["start"].item_field_label.text = "начало"
        elif opt.name == "start":
            if not val or int(val) >= int(end):
                self.options["start"].item_field_label.text_color = 1, 0,0,1
                self.options["start"].item_field_label.text = "начало" + " < конец"
            else:
                self.options["start"].item_field_label.text_color = 0.7, 0.7, 0.7, 1
                self.options["start"].item_field_label.text = "начало"
                self.options["end"].item_field_label.text_color = 0.7, 0.7, 0.7, 1
                self.options["end"].item_field_label.text = "конец"
        elif opt.name == "count":
            if not val or int(val) <= 0:
                self.options["count"].item_field_label.text_color = 1, 0,0,1
                self.options["count"].item_field_label.text = "количество" + " > 0"
            else:
                self.options["count"].item_field_label.text_color = 0.7, 0.7, 0.7, 1
                self.options["count"].item_field_label.text = "количество"

    def generate(self):
            if self.valid_value(self._options["start"],  self._options["end"], self._options["count"]):
                self._current_random_origin = self.random_generator_core.not_repeat(int(self._options["start"]),
                                                          int(self._options["end"]),
                                                          int(self._options["count"]))
                self.set_generator_label(self._current_random_origin)

            self.clean_text_field()

    def set_generator_label(self, _current_random_origin):
        self.label_random_text = self._options["sep"].join(_current_random_origin )
        self.ids.generator_label.text = self.label_random_text
        self.current_random = list(itertools.chain(*[list(x) for x in self._current_random_origin]))
        self.ids.generator_label.line_color_normal = 0.7, .7, .7, .4

    def valid_value(self, start, end, count):
        if all([start, end, count]) and count != "0" and end != "0" and int(end) > int(start):
            return True


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDIconButton


class Btn(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Img(Image, TouchBehavior):
    DIGIT = 'digits'
    IMAGE = 'images'

    def __init__(self, base_help_flag, **kwargs):
        super().__init__(**kwargs)
        self.duration_long_touch = 0.25
        self.base_help_flag = base_help_flag
        self.base_source = ""
        self.help_source = ""
        self.keys_source = ""

    def init_source(self):
        self.source = self.base_source if self.base_help_flag == Img.IMAGE else self.help_source

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.source = self.keys_source
            return
        if touch.y < 120.0:
            if self.base_help_flag == Img.IMAGE:
                self.source = self.help_source
            else:
                self.source = self.base_source
            super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.base_help_flag == Img.IMAGE:
            self.source = self.base_source
        else:
            self.source = self.help_source
        super().on_touch_up(touch)

    def on_long_touch(self, *args):
       if args[0].pos[1] > 121:
            self.source = self.keys_source

class MyImage(FloatLayout):
    def __init__(self, base_help_flag, name, **kwargs):
        """

        :param base_help_flag: str: MyImage.DIGIT or MyImage.IMAGE
        :param name:
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.name = name
        self.base_help_flag = base_help_flag

        self.image = Img(base_help_flag)
        self.add_widget(self.image)

        # self.btn = Btn(on_press=self.press_btn)
        # self.btn.icon = "resources/icons/yes.png"
        # self.btn.user_font_size = "20sp"
        # self.btn.pos_hint = {"right": 0.97, "center_y": .14}
        # self.add_widget(self.btn)

    def press_btn(self, v):
        print("press_btn")

    def init_source(self):
        self.image.init_source()

    def set_base_source(self, source):
        self.image.base_source = source

    def set_help_source(self, source):
        # print(source, "333333333")
        self.image.help_source = source

    def set_keys_source(self, source):
        # print(source, "333333333")
        self.image.keys_source = source

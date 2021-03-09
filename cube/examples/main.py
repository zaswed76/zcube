from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from core import seq

__VERSION__ = "0.0.07"

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()

class MyNavigationDrawer(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ContentNavigationDrawer(BoxLayout):
    pass
    def on_start(self):
       icons_item = {
           "folder": "My files",
           "account-multiple": "Shared with me",
           "star": "Starred",
           "history": "Recent",
           "checkbox-marked": "Shared with me",
           "upload": "Upload",
       }
       for icon_name in icons_item.keys():
           self.root.ids.content_drawer.ids.md_list.add_widget(
               ItemDrawer(icon=icon_name, text=icons_item[icon_name])
           )


    def update_status(self, *_):
        if self.status == "opening_with_swipe":
            MDApp.get_running_app().main.carusel.current_slide.blocked = True
            MDApp.get_running_app().main.carusel.ps = False
        else:
            MDApp.get_running_app().main.carusel.current_slide.blocked = False
            MDApp.get_running_app().main.carusel.ps = True
        super().update_status()


class MyImage(ButtonBehavior, Image):
    DIGIT = 'digits'
    IMAGE = 'images'

    def __init__(self, flag, name, **kwargs):
        super().__init__(**kwargs)
        self.blocked = False
        self._flag = flag
        self.help_flag = MyImage.DIGIT if self._flag == MyImage.IMAGE else MyImage.IMAGE
        self.name = name
        self.base_source = ""
        self.help_source = ""

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, flag):
        self.help_flag = MyImage.DIGIT if self._flag == MyImage.IMAGE else MyImage.IMAGE
        self._flag = flag

    def set_source(self):
        if self.flag == MyImage.IMAGE:
            self.source = self.base_source
        else:
            self.source = self.help_source

    def init_help_digit(self):
        s = "resources/{}/{}.png".format(self.help_flag, self.name)
        img = AsyncImage(source=s)
        img.size_hint = 1.2, 1.2
        self.add_widget(img)

    def on_touch_down(self, touch):
        if not self.blocked and touch.x > 200:
            if self._flag == MyImage.IMAGE:
                self.source = self.help_source
            else:
                self.source = self.base_source
        # super().on_touch_down(touch)

    def on_touch_up(self, touch):
            if self._flag == MyImage.IMAGE:
                self.source = self.base_source
            else:
                self.source = self.help_source

class CashContiner:
    def __init__(self, data_list: list):
        self._data_list = data_list.copy()
        self._data_list_copy = data_list.copy()

    # noinspection PyTypeChecker
    def get_widget(self, base_help_flag, helper_image_flag=False):
        lst = []
        for k in self._get_current_cash():
            _object = MyImage(base_help_flag, str(k))
            _object.base_source = "resources/images/{}.png".format(k)
            _object.help_source = "resources/digits/{}.png".format(k)
            _object.set_source()
            if helper_image_flag:
                _object.init_help_digit()
            lst.append(_object)

        return lst

    def _get_current_cash(self, count=2):
        return [str(self._data_list.pop(0)) for _ in range(count) if self._data_list]

    def set_data(self, data):
        self._data_list = data.copy()


class MyCarousel(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ps = True

    def on_touch_move(self, touch):
        if self.ps:
            super().on_touch_move(touch)

    def on_index(self, *args):
        MDApp.get_running_app().next_slide(self.index)
        Carousel.on_index(self, *args)

class ContentNavigationDrawer(BoxLayout):
    pass

class MainBox(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base_help_flag = MyImage.IMAGE
        self.helper_image_flag = False
        self.shuffle = False
        self.seq = seq.Seq()
        self.seq.set_data(0, 10)
        self.cash_conteiner = CashContiner(self.seq.data)
        self.carusel = MyCarousel()
        # self.carusel.loop = True
        self.carusel.anim_move_duration = 0.4
        self.carusel.scroll_timeout = 100
        self.carusel.size_hint = 1, 0.9
        self.carusel.min_move = 0.05
        lb = MDLabel(text="v={}".format(__VERSION__))
        lb.pos_hint = {'top':1}
        lb.size_hint = 1, 0.05
        self.mainwidget.add_widget(lb)
        self.mainwidget.add_widget(self.carusel)

    def new_list(self):
        self.seq.set_data(10, 20)
        self.start_carousel()

    def shuffle_check_active(self, active):
        if active:
            self.seq.shuffle()
            self.start_carousel()
        else:
            self.seq.sort()
            self.start_carousel()

    def start_carousel(self):
        print("!!!!!!!!!!!!!")
        self.cash_conteiner.set_data(self.seq.data)
        self.carusel.clear_widgets()
        self.load_to_carousel()

    def load_to_carousel(self):
        for widget in self.cash_conteiner.get_widget(self.base_help_flag, self.helper_image_flag):
            self.carusel.add_widget(widget)

    def touch(self, t):
        self.carusel.ps = True

    def nottouch(self, t):
        self.carusel.ps = False

    def help_active(self, active):
        if active:
            self.helper_image_flag = True
            self.start_carousel()
        else:
            self.helper_image_flag = False
            self.start_carousel()

    def checkbox_active(self, v):
        if v:
            self.base_help_flag = MyImage.DIGIT
            self.start_carousel()
        else:
            self.base_help_flag = MyImage.IMAGE
            self.start_carousel()

class MainBoxApp(MDApp):
    def build(self):
        self.main = MainBox()
        self.main.load_to_carousel()
        return self.main

    def next_slide(self, index):
        self.main.load_to_carousel()

if __name__ == '__main__':
    MainBoxApp().run()

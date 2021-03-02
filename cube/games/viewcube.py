import os

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class MyButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dir_digit = "resources/digit"

        self._source = self.source
        self.name = None

    def init_help_digit(self):
        self.box = AnchorLayout()
        self.add_widget(self.box)
        img = AsyncImage(source="resources/digit/{}".format(self.convert_name(self.name)))
        img.size_hint = 1.2, 1.2
        self.box.add_widget(img)

    def on_press(self):
        path_img = os.path.join(self.dir_digit, self.convert_name(self.name))
        self.source = path_img

    def convert_name(self, name):
        if len(self.name) == 1:
            nameimg = "00" + self.name + ".png"
        else:
            nameimg = "0" + self.name + ".png"
        return nameimg

    def on_release(self):
        self.source = self._source


class MyCarousel(Carousel):
    def on_index(self, *args):
        MDApp.get_running_app().next_slide(self.index)
        Carousel.on_index(self, *args)


class ViewCube(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.permanent_help_flag = False
        self.cash_list = []
        self._current_cash = []

    def init_carousel(self):
        self.app = MDApp.get_running_app()
        self.carousel = MyCarousel(direction='right')
        self.carousel.anim_move_duration = 0.5
        self.carousel.scroll_timeout = 100
        self.carousel.size_hint = 1, 0.9
        self.carousel.min_move = 0.1

        self.add_widget(self.carousel)
        self.imge_cash = {}

    def creat_image_btns(self, lst):
        for i in lst:
            if i not in self.imge_cash:
                src = f"resources/images/{i}.png"
                image = MyButton(source=src, allow_stretch=True)
                image.name = str(i)
                if self.permanent_help_flag:
                    image.init_help_digit()
                self.imge_cash[i] = image

    def add_in_carusel(self, cash):
        nlist = [x.name for x in self.carousel.slides]
        for k in cash:
            if k not in nlist:
                self.carousel.add_widget(self.imge_cash[k])


    def load_image(self, img_list):
        self.carousel.clear_widgets()
        cash = self.create_cash()
        self.creat_image_btns(cash)
        for k in cash:
            self.carousel.add_widget(self.imge_cash[k])

    def get_seq(self, start, end):
        return range(start, end)

    def callback_home(self, v):
        self.manager.current = "menu"

    def callback_back(self, v):
        self.carousel.clear_widgets()
        self.manager.current = "imageviewgrid"


    def sort(self, v):
        self.app.seq.sort()
        self.app.select(self.app.seq.data)

    def hide_help_digit(self, v):
        if self.permanent_help_flag:
            for c in self.imge_cash.values():
                c.clear_widgets()
            self.permanent_help_flag = False

        else:
            self.show_help_digit()
            self.permanent_help_flag = True
        self.app.stored_data.put("view", permanent_help=self.permanent_help_flag)

    def show_help_digit(self):
        for c in self.imge_cash.values():
            c.init_help_digit()

    def create_cash(self, count=2):
        self._current_cash =  [str(self.cash_list.pop(0)) for _ in range(count) if self.cash_list]

    @property
    def current_cash(self):
        return self._current_cash

import os

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar


class MyButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dir_digit = "resources/digit"
        self.dir_image = "resources/images"

        self.name = None
        self.image_numeric_flag = None

    def set_source(self):
        print(self.image_numeric_flag, "333333333333333333333")
        self.source = "resources/{}/{}.png".format(self.image_numeric_flag, self.name)

    def init_help_digit(self):
        if self.image_numeric_flag == "images":
            help_dir = self.dir_digit
        else:
            help_dir = self.dir_image
        img = AsyncImage(source="{}/{}.png".format(help_dir, self.name))
        img.size_hint = 1.2, 1.2
        self.add_widget(img)

    def on_press(self):
        if self.image_numeric_flag == "images":
            help_dir = self.dir_digit
        else:
            help_dir = self.dir_image
        path_img = "{}/{}.png".format(help_dir, self.name)
        self.source = path_img



    def on_release(self):
        if self.image_numeric_flag == "images":
            help_dir = self.dir_image
        else:
            help_dir = self.dir_digit
        path_img = "{}/{}.png".format(help_dir, self.name)
        self.source = path_img


class MyCarousel(Carousel):
    def on_index(self, *args):
        MDApp.get_running_app().next_slide(self.index)
        Carousel.on_index(self, *args)


class ViewCube(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.permanent_help_flag = False
        self.image_numeric_flag = None
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
        self.progerss = MDProgressBar()
        self.progerss.value = 0
        self.progerss.size_hint = 1, 0.2
        self.progerss.pos_hint = {'center_y': 0.009}
        self.view_float_box.add_widget(self.progerss)
            # pos_hint: {'bottom':0}


    def creat_image_btns(self, lst, image_numeric_flag):
        for i in lst:
            if i not in self.imge_cash:
                image = MyButton()
                image.name = str(i)
                image.image_numeric_flag = image_numeric_flag
                image.set_source()
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




    def hide_help_digit(self, v):
        if self.permanent_help_flag:
            for c in self.carousel.slides:
                c.clear_widgets()
            self.permanent_help_flag = False

        else:
            self.show_help_digit()
            self.permanent_help_flag = True
        self.app.stored_data.put("view", permanent_help=self.permanent_help_flag)

    def show_help_digit(self):
        for c in self.carousel.slides:
            c.init_help_digit()

    def create_cash(self, count=2):
        self._current_cash =  [str(self.cash_list.pop(0)) for _ in range(count) if self.cash_list]

    @property
    def current_cash(self):
        return self._current_cash

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from screens.image import MyImage, Img


class CheckButton(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parent = None
        self.checked = False
        self.icon_checked = ""
        self.icon_unchecked = ""
        self. user_font_size = "6sp"
        self.pos_hint = {"center_x": .5, "center_y": .5}
        # self.update()

    def update(self):
        if self.checked:
            self.icon = self.icon_checked
        else:
            self.icon = self.icon_unchecked

    def on_press(self):
        self.checked = not self.checked
        # MDApp.get_running_app().view.set_cycle(self.checked)
        self.update()




class CashContiner:
    def __init__(self, data_list: list, image_dir=""):
        self.image_dir = image_dir
        self._data_list = data_list.copy()
        self._data_list_copy = data_list.copy()
        self._cursor = 0


    # noinspection PyTypeChecker
    def get_widget(self, base_help_flag, helper_image_flag=False):
        lst = []
        for k in self._get_current_cash():
            _object = MyImage(base_help_flag, str(k))
            img = "{}/{}/{}.png".format(self.image_dir, "base", k)
            print(img)
            _object.set_base_source(img)
            _object.set_help_source("{}/{}/{}.png".format(self.image_dir, "helper", k))
            _object.set_keys_source("{}/{}/{}.png".format(self.image_dir, "helper_key", int(k/10)*10))
            _object.init_source()
            if helper_image_flag:
                _object.init_help_digit()
            lst.append(_object)
        return lst

    def _get_current_cash(self, count=2):
        res = []
        for _ in [0, 1]:
            try:
                res.append(self._data_list[self._cursor])
            except IndexError:
                return []
            self._cursor += 1
        return res


    def set_data(self, data):
        self._cursor = 0
        self._data_list.clear()
        self._data_list = data.copy()


class MyCarousel(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._len_data = 0
        self.cindex = 0
        self.cycle = False
        self.gcount = 0



    @property
    def len_data(self):
        return self._len_data

    @len_data.setter
    def len_data(self, ln):
        self._len_data = ln-1

    def on_index(self, *args):
        self.gcount += 1
        self.cindex = args[1]
        if args[1] != 0:
            MDApp.get_running_app().view.load_to_carousel(args[1])
        elif args[1] is None:
            pass

        Carousel.on_index(self, *args)

    def on_touch_move(self, touch):
        if self.cindex == self.len_data and self.cycle:
            self.load_slide(self.slides[0])
        super().on_touch_move(touch)

class View(Screen):
    def __init__(self, seq, stored_data, image_dir="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = 1 ,1


        self.stored_data = stored_data
        self.image_dir = image_dir
        self.base_help_flag = self.stored_data.get("ui")["base_help_flag"]
        self.helper_image_flag = False
        self.shuffle = self.stored_data.get("ui")["shuffle"]
        self.seq = seq

        self.cash_conteiner = CashContiner(self.seq.data, image_dir=self.image_dir)
        self.carusel = MyCarousel()
        self.carusel.cycle = self.stored_data.get("ui").get("cycle")
        self.carusel.anim_move_duration = 0.25
        self.carusel.scroll_timeout = 100
        self.carusel.size_hint = 1, 0.9
        self.carusel.min_move = 0.04
        self.carusel.scroll_distance = 20
        self.mainwidget.add_widget(self.carusel)

        self.cycle = self.stored_data.get("ui")["cycle"]
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.set_color((1, 1, 1, 1))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_color(self, color):
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def set_image_dir(self, path):
        self.image_dir = path
        self.cash_conteiner = CashContiner(self.seq.data, image_dir=self.image_dir)

    def set_cycle(self, checked):

        self.carusel.cycle = checked
        self.cycle = checked

    def start_carousel(self):
        if self.shuffle:
            self.seq.shuffle()
        else:
            self.seq.sort()

        self.cash_conteiner.set_data(self.seq.data)
        self.carusel.len_data = len(self.seq.data)
        self.carusel.cindex = 0
        self.carusel.clear_widgets()
        self.load_to_carousel(0)

    def new_list(self):
        self.seq.set_data(0, 10)
        self.start_carousel()

    def image_num(self, active):
        if active:

            self.base_help_flag = Img.IMAGE
        else:

            self.base_help_flag = Img.DIGIT


        self.start_carousel()


    def shuffle_check_active(self, active):
        if active:
            self.shuffle = True
            self.start_carousel()
        else:
            self.shuffle = False
            self.start_carousel()

    def load_to_carousel(self, index):
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






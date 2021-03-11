import os

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior, RectangularRippleBehavior, BackgroundColorBehavior
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.window import Window


class ImageButton(RectangularRippleBehavior, TouchBehavior, ButtonBehavior, Image, BackgroundColorBehavior):
    selected_flag = False
    selected_count = 0

    def __init__(self, name, image_path, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.orientation = "vertical"
        self.image_path = image_path
        self.size_hint = 1, None
        self.height = Window.size[1] / 6
        self.radius = 0
        self.elevation = 0
        self.source = self.image_path

        self._select = False
        self.md_bg_color = [1, 1, 1, 1]

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, state):
        self._select = state
        if self.select:
            ImageButton.selected_count += 1
            self.md_bg_color = [0, .9, .9, 1]
        else:
            ImageButton.selected_count -= 1
            self.md_bg_color = [1, 1, 1, 1]

        if ImageButton.selected_count > 0:
            ImageButton.selected_flag = True
        else:
            ImageButton.selected_flag = False


    def on_double_tap(self, *args):
        print("<on_double_tap> event")

    def on_long_touch(self, *args):
        if not self.select and ImageButton.selected_count == 0:
            ImageButton.selected_flag = True
            self.select = True

    def on_press(self):
        if ImageButton.selected_flag:
            if not self.select:
                self.select = True
            else:
                self.select = False
                if ImageButton.selected_count == 0:
                    ImageButton.selected_flag = False
        else:
            print("run")


class ImageGrid(Screen):
    def __init__(self, checked, base_dir="base", **kw):
        super().__init__(**kw)
        self.checked = checked
        # print(self.checked, "self.checked")

        self.base_dir = base_dir
        self.image_dir = ""
        self.work_dir = ""

    def init_grid_image(self, image_dir, base_dir="base", parts=10):
        if not parts:
            parts = 10
        self.image_grid_layout.clear_widgets()
        self.image_grid_layout.cols = 3
        if image_dir and base_dir:
            self.work_dir = os.path.join(image_dir, base_dir)
            if os.path.isdir(self.work_dir):
                n_images = len(os.listdir(self.work_dir))
                for i in range(0, 100, int(n_images / int(parts))):
                    i = str(i)
                    name = str(i) + ".png"
                    image_path = os.path.join(self.work_dir, name)
                    if os.path.isfile(image_path):
                        btn = ImageButton(i, image_path)
                        if i in self.checked:
                            btn.select = True

                        self.image_grid_layout.add_widget(btn)

    def get_checked_widgets(self):
        return [b.name for b in self.image_grid_layout.children if b.select]

    def get_checked(self):
        r = {btn.name: btn.select for btn in self.image_grid_layout.children}
        # print(r, "!!!!!!!!!!!!!!!!!!!!")
        return r

    def select_group(self, v):
        state = True if v else False
        ImageButton.selected_flag = False
        ImageButton.selected_count = 0
        for btn in self.image_grid_layout.children:
            btn.select = state
        if not state:
            ImageButton.selected_count = 0
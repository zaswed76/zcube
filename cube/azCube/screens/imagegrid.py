import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox


class ImageButton(MDCard):
    def __init__(self, name, image_path, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.orientation = "vertical"
        self.image_path = image_path
        self.size_hint = 1, None
        self.height = 120
        self.radius = 0
        self.elevation = 0

        self.image = Image(source=self.image_path)
        self.check_button = MDCheckbox()

        box_for_check = BoxLayout()
        box_for_check.size_hint = None, None
        box_for_check.size = 100, 50
        box_for_check.pos_hint = {"right": 1, "bottom": 1}

        box_for_check.add_widget(Widget())
        box_for_check.add_widget(self.check_button)

        self.add_widget(self.image)
        self.add_widget(box_for_check)


class ImageGrid(Screen):
    def __init__(self, checked, base_dir="base", **kw):
        super().__init__(**kw)
        self.checked = checked
        print(checked, "checked")
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
                for i in range(0, 100, int(n_images / parts)):
                    i = str(i)
                    name = str(i) + ".png"
                    image_path = os.path.join(self.work_dir, name)
                    if os.path.isfile(image_path):
                        btn = ImageButton(i, image_path)
                        if i in self.checked:
                            btn.check_button.state = "down"
                        self.image_grid_layout.add_widget(btn)

    def get_checked_widgets(self):
        return [b.name for b in self.image_grid_layout.children if b.check_button.state == "down"]

    def get_checked(self):
        return {btn.name: btn.check_button.state for btn in self.image_grid_layout.children}

    def select_group(self, v):
        state = "down" if v else "normal"
        for btn in self.image_grid_layout.children:
            btn.check_button.state = state

import os
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage

from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.screenmanager import Screen


class Check(MDCheckbox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = None
        self.size_hint = None, None
        self.size = "40dp", "40dp"

class ImageCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint =  1, None
        self.height = 120
        self.soorce_img = None
        self.name = None
        self.box = GridLayout()
        self.box.padding = 5, 5, 0, 0
        self.box.rows = 2
        self.add_widget(self.box)

    def init(self):
        self.imgbtn = ImageButton(source = self.soorce_img)
        self.imgbtn.name = self.name
        self.box.add_widget(self.imgbtn)
        self.check = Check()
        self.check.name = self.name
        b = BoxLayout()
        left = Widget()
        b.add_widget(left)
        b.add_widget(self.check)
        self.box.add_widget(b)



class ImageButton(AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint =  None, None
        self.size = 50, 50
        # self.size_hint =  None, None
        self.name = None






class ImageViewGrid(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.image_dir = "resources/keys"
        self.active_checks = []

    def set_seq(self, seq):
        self.seq = seq

    def init_grid_image(self, data):
        self.image_grid_layout.cols = 3
        for i in range(10):
            name = str(i) + ".png"
            img_path = os.path.join(self.image_dir, name)
            btn = ImageCard()
            btn.soorce_img = img_path
            btn.name = str(i)
            btn.init()
            btn.imgbtn.bind(on_press=self.app.run_view)
            d = data[str(i)]
            btn.check.active = d
            btn.check.bind(active=self.on_checkbox_active)
            self.image_grid_layout.add_widget(btn)

    def on_checkbox_active(self, check, value):
        self.active_checks.clear()
        for card in self.image_grid_layout.children:
            if card.check.active:
                self.active_checks.append(card.check.name)
        self.seq.set_data_on_seq(self.active_checks)
        self.app.save(self.active_checks)


    # def run_view(self, v):
    #     if self.seq.data:
    #         self.app.run_view(self.seq.data)

    def select_all(self, select_flag):
        for card in self.image_grid_layout.children:
            card.check.active = select_flag

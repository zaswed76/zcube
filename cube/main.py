
__version__ = "0.1.15"

from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

from games.imageviewgrid import ImageViewGrid
from games.viewcube import ViewCube

Builder.load_file("kv/mainbox.kv")
from kivy.core.window import Window

from core.seq import Seq





class MScreenManager(ScreenManager):
    pass

class MenuScreen(Screen):
    pass

class GamesScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        btn = Button(text="menu")
        btn.bind(on_press=self.home_press)
        self.setting_main_box.add_widget(btn)

    def set_version_label(self, v, size):
        lv_version = Button(text="version {}\n{}".format(v, size))
        lv_version.font_size = "20sp"
        self.setting_main_box.add_widget(lv_version)



    def home_press(self, v):
        self.manager.current = "menu"

class MainBoxApp(MDApp):
    def build(self):
        self.stored_data = JsonStore('data/data.json')
        self.check_data = self.stored_data.get("checked")
        self.permanent_help_flag = self.stored_data.get("view")["permanent_help"]
        self.seq = Seq()

        true_checks = [k for k in self.check_data if self.check_data[k]]
        self.seq.set_data_on_seq(true_checks)
        self.sm = MScreenManager()


        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(GamesScreen(name='games'))

        self._init_settings_screen()
        self._init_image_view_grid()
        self._init_viewcube()
        return self.sm

    def _init_viewcube(self):
        self.viewcube = ViewCube(name='viewcube')
        self.viewcube.permanent_help_flag = self.permanent_help_flag
        self.viewcube.init_carousel()
        self.viewcube.creat_image_btns()
        self.sm.add_widget(self.viewcube)

    def _init_image_view_grid(self):
        self.image_view_grid = ImageViewGrid(name='imageviewgrid')
        self.image_view_grid.init_grid_image(self.check_data)
        self.image_view_grid.set_seq(self.seq)
        self.sm.add_widget(self.image_view_grid)

    def _init_settings_screen(self):
        self.settings_screen = SettingsScreen(name='settings')
        self.settings_screen.set_version_label(__version__, str(Window.size))
        self.sm.add_widget(self.settings_screen)

    def run_view(self, v):
        img_list = self.seq.data
        self.sm.current = "viewcube"
        self.viewcube.load_image(img_list)

    def next_slide(self, index):
        if index is not None:
            print(self.seq.data[index], "!!!!")

    def select_group(self, select_flag):
        self.image_view_grid.select_all(select_flag)



    def save(self, data_list):
        for name in self.check_data:
            if name in data_list:
                self.check_data[name] = True
            else:
                self.check_data[name] = False
        self.stored_data.put("checked", **self.check_data)



    def stop(self, *largs):
        super().stop()
if __name__ == '__main__':
    MainBoxApp().run()
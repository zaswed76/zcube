from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, OneLineAvatarIconListItem, IRightBodyTouch, IconLeftWidget

__version__ = "0.1.59"
# ------------------------------------------------------
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.filemanager import MDFileManager

if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
    except:
        pass
else:
    Window.size = (400, 700)

from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout

from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from screens.imagegrid import ImageGrid
from screens.view import View, CashContiner
from screens.keywiew import KeysView
# from screens.settings import RV

from kivy.lang import Builder

from core import seq

Builder.load_file("kv/imagegrid.kv")


class MScreenManager(ScreenManager):
    pass


class ListItem(BoxLayout):
    def __init__(self, text, field=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.option_label.text = text
        if field is not None:
            self.ids.option_field.text = str(field)


class SettingsView(Screen):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.options = {}
        self.store = store
        items = ["parts"]
        for i in items:
            self.options[i] = ListItem(str(i), self.store.get("ui").get("parts"))
            self.settings_box.add_widget(self.options[i])
        self.settings_box.add_widget(Label())


class Store(JsonStore):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)

    def get(self, key):
        return self._data.get(key, {})


class MainBoxApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version = __version__
        self.current_screen = None
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        self.seq = seq.Seq()


        self.stored_data = Store('data/data.json')
        self.image_grid_parts = self.stored_data.get("ui").get("parts")
        self.images_dir = self.stored_data.get("ui").get("images_dir")
        self.dialog = None
        self.screen_manager = MScreenManager()

    def build(self):
        self._init_settings_screen()
        self._init_view()
        self._init_keys_view()
        self._init_image_grid()

        if self.valid_settings:
            self.screen_manager.current = "image_grid"
        else:
            self.screen_manager.current = "settings_view"
        return self.screen_manager

    # --------------------------------------------------------------

    @property
    def valid_settings(self):
        flag = False
        if self.stored_data.get("ui").get("parts"):
            flag = True
        return flag

    def exit_manager(self, *args):
        self.file_manager.close()

    def file_manager_open(self):
        if platform == "android":
            p = "/storage/emulated/0"
        else:
            p = "/"
        self.file_manager.show(p)  # output manager to the screen

    def select_path(self, path):
        self.exit_manager()
        self.images_dir = path
        self.view.set_image_dir(self.images_dir)
        self.view.new_list()
        self.image_view_grid.init_grid_image(self.images_dir, parts=self.image_grid_parts)

    # --------------------------------------------------------------------

    def _init_view(self):
        self.view = View(self.seq, self.stored_data, image_dir=self.images_dir, name='view')
        self.view.set_image_dir(self.images_dir)
        self.view.start_carousel()
        self.screen_manager.add_widget(self.view)

    def _init_keys_view(self):
        self.keys_view = KeysView(name='keys_view')
        self.screen_manager.add_widget(self.keys_view)

    def _init_image_grid(self):
        checked = [k for k, v in self.stored_data.get("ui")["checked"].items() if v]
        self.image_view_grid = ImageGrid(checked, name='image_grid')
        self.images_dir = self.stored_data.get("ui").get("images_dir")
        base_dir = self.stored_data.get("ui").get("base_dir")
        parts = self.stored_data.get("ui").get("parts")
        self.image_view_grid.init_grid_image(self.images_dir, base_dir, parts=parts)
        self.screen_manager.add_widget(self.image_view_grid)

    def _init_settings_screen(self):
        self.settings_view = SettingsView(self.stored_data, name='settings_view')
        self.screen_manager.add_widget(self.settings_view)

    def run_view(self, v):
        self.current_screen = "view"
        check_list = self.image_view_grid.get_checked_widgets()
        if check_list:
            self.view.set_image_dir(self.images_dir)
            self.view.seq.set_data_on_seq(check_list)
            self.view.shuffle = self.view.shuffle_checked.checked
            self.view.start_carousel()
            self.screen_manager.current = "view"

    def run_grid_image(self, v):

        self.current_screen = "image_grid"
        self.screen_manager.current = "image_grid"
        parts = self.settings_view.options.get("parts").ids.option_field.text
        base_dir = self.stored_data.get("ui").get("base_dir")
        self.image_view_grid.init_grid_image(self.images_dir, base_dir, parts=parts)
        self.image_view_grid.select_group(False)


    def run_settings_view(self, v):
        self.screen_manager.current = "settings_view"

    def run_back(self, x):


        if self.current_screen is not None:
            self.screen_manager.current = self.current_screen
        else:
            self.run_grid_image(0)

    def run_keys_view(self, x):
        self.screen_manager.current = "keys_view"

    def stop(self, *args):
        self.save_store(0)
        super().stop(*args)

    def save_store(self, x):
        checked = self.image_view_grid.get_checked()
        cycle = self.view.loop_checked.checked
        shuffle = self.view.shuffle_checked.checked
        images_dir = self.view.image_dir
        base_dir = "base"
        parts = 10
        image_num_checked = self.view.image_num_checked.checked
        base_help_flag = self.view.base_help_flag
        save_dict = dict(checked=checked, cycle=cycle,
                         images_dir=images_dir, base_dir=base_dir,
                         parts=parts, image_num_checked=image_num_checked,
                         shuffle=shuffle, base_help_flag=base_help_flag)
        self.stored_data.put("ui", **save_dict)

    def select_group(self, select):
        self.image_view_grid.select_group(select)


if __name__ == '__main__':
    MainBoxApp().run()

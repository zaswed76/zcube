__version__ = "0.1.52"
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

from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from screens.imagegrid import ImageGrid
from screens.view import View, CashContiner

from kivy.lang import Builder

from core import seq

Builder.load_file("kv/imagegrid.kv")


class MScreenManager(ScreenManager):
    pass


class SettingsView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ContentDialog(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "4dp"
        self.size_hint_y = None
        self.height = "30dp"
        self.mdtext = MDTextField()
        self.add_widget(self.mdtext)


class Store(JsonStore):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)

    def get(self, key):
        return self._data.get(key, {})


class MainBoxApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version = __version__
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        self.seq = seq.Seq()


        self.stored_data = Store('data/data.json')
        self.images_dir = None
        self.dialog = None
        self.screen_manager = MScreenManager()

    # --------------------------------------------------------------

    def exit_manager(self):
        self.file_manager.close()

    def file_manager_open(self):
        if platform == "android":
            p = "/storage/emulated/0"
        else:
            p = "/"
        self.file_manager.show(p)  # output manager to the screen

    def select_path(self, path):
        self.exit_manager()
        self.show_confirmation_dialog()
        self.images_dir = path
        self.view.set_image_dir(self.images_dir)
        self.view.new_list()

    # --------------------------------------------------------------------
    def show_confirmation_dialog(self):
        if not self.dialog:
            content_cls = ContentDialog()
            self.dialog = MDDialog(
                title="укажите на сколько частей\nразделить изображения:",
                type="custom",
                content_cls=content_cls,
                buttons=[

                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,
                        on_press=lambda a: self.dialog_ok(content_cls.mdtext)
                    ),
                ],
            )
        self.dialog.open()

    def dialog_ok(self, widget):
        self.dialog.dismiss(force=True)
        try:
            p = int(widget.text)
        except ValueError:
            p = 10
        # self.stored_data.put("parts", parts=p)
        self.create_image_grid(p)

    def create_image_grid(self, parts):
        self.image_view_grid.init_grid_image(self.images_dir, parts=parts)

    def build(self):
        self._init_image_grid()
        self._init_view()
        self._init_settings_screen()
        self.screen_manager.current = "image_grid"
        return self.screen_manager

    def _init_view(self):
        self.view = View(self.seq, self.stored_data, image_dir=self.images_dir, name='view')
        checked = [k for k, v in self.stored_data.get("ui")["checked"].items() if v == "down"]
        # self.view.seq.set_data_on_seq(checked)
        self.view.set_image_dir(self.images_dir)
        self.view.start_carousel()

        self.screen_manager.add_widget(self.view)

    def _init_image_grid(self):
        checked = [k for k, v in self.stored_data.get("ui")["checked"].items() if v == "down"]
        self.image_view_grid = ImageGrid(checked, name='image_grid')
        self.images_dir = self.stored_data.get("ui").get("images_dir")
        base_dir = self.stored_data.get("ui").get("base_dir")
        parts = self.stored_data.get("ui").get("parts")
        self.image_view_grid.init_grid_image(self.images_dir, base_dir, parts=parts)
        self.screen_manager.add_widget(self.image_view_grid)

    def _init_settings_screen(self):
        self.settings_view = SettingsView(name='settings_view')
        self.screen_manager.add_widget(self.settings_view)

    def run_view(self, v):
        check_list = self.image_view_grid.get_checked_widgets()
        if check_list:
            self.view.seq.set_data_on_seq(check_list)
            self.view.shuffle = self.view.shuffle_checked.checked


            self.view.start_carousel()

            self.screen_manager.current = "view"

    def run_grid_image(self, v):
        self.screen_manager.current = "image_grid"

    def run_settings_view(self, v):
        self.screen_manager.current = "settings_view"

    def stop(self, *args):
        self.save_store()
        super().stop()

    def save_store(self):

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


if __name__ == '__main__':
    MainBoxApp().run()

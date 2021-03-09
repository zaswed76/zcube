from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton


class IconButton(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked = False
        self.checked_icon = ""
        self.unchecked_icon = ""

    def update(self):
        if self.checked:
            self.icon = self.unchecked_icon
        else:
            self.icon = self.checked_icon

    def on_press(self):
        self.checked = not self.checked
        self.update()
        super().on_press()
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Hotkeys(ABC):

    def home(self):
        self.phone.input_keyevent(3)

    def clear_recent_apps(self):
        self.phone.input_keyevent('KEYCODE_APP_SWITCH')
        self.phone.input_tap(482, 41)

    def scroll_down(self):
        self.phone.input_swipe(400, 400, 400, 300, 100)

    def recent_apps(self):
        self.phone.input_keyevent('KEYCODE_APP_SWITCH')

    @property
    def phone(self):
        return

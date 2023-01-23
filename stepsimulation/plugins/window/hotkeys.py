import pyautogui
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


# TODO
# add: win32gui.MoveWindow(hwnd, 0, 0, 593, 1020, True)

@dataclass
class Hotkeys(ABC):
    def arrange(self):
        fixed_position = (0, 0)
        fixed_size = (593, 1020)

        if self.window.topleft != fixed_position:
            self.window.moveTo(fixed_position[0], fixed_position[1])

        if self.window.size != fixed_size:
            self.window.resizeTo(fixed_size[0], fixed_size[1])

    @staticmethod
    def trim():
        pyautogui.hotkey('ctrl', 'shiftleft', 't')

    @property
    def window(self):
        """ return window property"""
        return

import subprocess
import time
import numpy
import os

import pyautogui, pygetwindow
import win32api, win32con, win32gui

from dataclasses import dataclass, field

from plugins.window.hotkeys import Hotkeys

from utils.decorators import timer

pyautogui.PAUSE = 0.5


@dataclass(kw_only=True)
class Window(Hotkeys):
    title: str
    status: any = field(default=None)

    process: subprocess.Popen = field(init=False)
    window: pygetwindow = field(default=pygetwindow)

    def create(self, account_number: str) -> None:

        path = os.path.join(os.environ["ProgramFiles"], 'BlueStacks_nxt', 'HD-Player.exe --instance Nougat64')

        if str(account_number) != "1":
            path += f"_{int(account_number) + 1}"

        self.process = subprocess.Popen(path)

    @timer(timeout=30, sleep=1)
    def is_process(self, state='start') -> bool:
        tasklistrl = os.popen("tasklist").read().split()

        if state == 'start':
            if str(self.process.pid) in tasklistrl:
                return True

        elif state == 'stop':
            if str(self.process.pid) not in tasklistrl:
                return True

    def get_window(self) -> bool:
        window = pyautogui.getWindowsWithTitle(self.title)

        if window is None:
            print("No window available, run start() first")
            return False

        self.window = window

        titles = pyautogui.getAllTitles()
        for title in titles:
            if self.title == title:
                self.window = pyautogui.getWindowsWithTitle(self.title)[0]
                return True
        return False

    @staticmethod
    def left_click(hwnd, pos):
        lParam = win32api.MAKELONG(pos[0], pos[1])

        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(0.1)

    def find_close_btn(self, region: tuple[int, int]) -> tuple[int, int]:
        # make screenshot
        image = pyautogui.screenshot(region=region)

        # convert screenshot to array
        image = numpy.array(image, dtype=numpy.uint8)

        # find matching pixels
        pixel_color = [235, 85, 62]
        for i in range(0, len(image), 5):
            for j in range(0, len(image[i]), 5):
                if list(image[i][j]) == pixel_color:
                    return j, i

    def close(self) -> bool:
        # call close signal
        process = subprocess.call(f"TASKKILL /PID {self.process.pid}", stdout=subprocess.DEVNULL)
        # print(process)
        time.sleep(0.5)

        # check if promotion popped up
        if 'BlueStacks Exit Window' in pyautogui.getAllTitles():
            close_whndl = win32gui.FindWindowEx(0, 0, None, f'BlueStacks Exit Window')

        # get close window handle
        else:
            close_whndl = win32gui.FindWindowEx(0, 0, None, f'Close {self.title}')

        # check if handle exists
        if close_whndl == 0:
            return False

        for _ in range(30):
            if f'Close {self.title}' in pyautogui.getAllTitles():
                break
            else:
                time.sleep(1)

        # find window coords
        region = win32gui.GetWindowRect(close_whndl)

        # find btn coords
        dx, dy = self.find_close_btn(region)

        # click close btn
        self.left_click(close_whndl, (dx, dy))

        return True

    @staticmethod
    def terminate() -> None:
        print('TERMINATE')
        process = subprocess.call('wmic process where name="HD-Player.exe" delete', stdout=subprocess.DEVNULL)
        # print(process)
        time.sleep(5)

        # from stepsimulation.core.listener.listener import upload
        # upload({
        #     "number": "0",
        #     "state": "Off",
        #     "app": "Off",
        #     "close": "",
        #     "updated": "False",
        #     "timestamp": f"{date.today().strftime('%Y%m%d')}"
        # })

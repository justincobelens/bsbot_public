from dataclasses import dataclass, field

from window import Window
from phone import Phone



@dataclass(kw_only=True)
class PlayerData:
    number: str
    name: str

    def __post_init__(self):
        self.title = f"{self.number} - {self.name}"


@dataclass(kw_only=True)
class Player(PlayerData):
    window: Window = field(init=False)
    phone: Phone = field(init=False)

    def start(self) -> list[[bool, str]]:
        error_msg = [True, 'no_error']

        print(f"\n** starting {self.number} **")

        # TODO
        # Add try/except

        # initiate window/phone obj
        self.window = Window(title=self.title)
        self.phone = Phone()

        # create bluestacks instance
        self.window.create(self.number)

        # check if instance is created
        if not self.window.is_process(state='start'):
            error_msg = [False, 'window_is_process']
            return error_msg

        # check if phone is connected
        if not self.phone.is_connected(self.number):
            error_msg = [False, 'phone_connect']
            return error_msg

        # check if phone is ready to use
        if not self.phone.is_ready():
            error_msg = [False, 'phone_ready']
            return error_msg

        # rearrange window
        self.window.get_window()
        self.window.arrange()

        return error_msg

    def stop(self) -> list[[bool, str]]:
        error_msg = [True, 'no_error']

        print(f"** stopping {self.number} **")

        # stop window
        self.window.close()

        if not self.window.is_process(state='stop'):
            error_msg = [False, 'window_is_stopping_process']
            return error_msg

        # if self.window.kill() is False:
        #     error_msg = [False, 'kill_error']

        # stop phone
        self.phone.disconnect()

        return error_msg

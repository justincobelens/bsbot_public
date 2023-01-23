'''import inspect

from dataclasses import dataclass, asdict, field
from datetime import date


@dataclass()
class Player:
    number: int
    state: str
    app: str
    close_signal: str

    updated: bool = field(default=False)

    timestamp: date = field(default=date.today().strftime("%Y%m%d"))

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    def update_number(self, words) -> None:

        # get lines with enough words to prevent IndexErrors
        if len(words) <= 6:
            return

        # define number variable and item in list that has number in it
        nougat = words[5]

        # check if word is actually "Nougat"
        if nougat[:6] != 'Nougat':
            return

        # get current number
        if nougat == 'Nougat64':
            new_number = 1
        else:
            new_number = int(nougat[9:]) - 1

        # check if number actually changed, otherwise no return statement is needed
        if self.number != new_number:
            self.number = new_number
            self.updated = True

    def update_state(self, words) -> None:
        # define state variables
        new_state = self.state

        if "Player" and "state" in words:
            if "[Stopping]" in words:
                new_state = 'Off'


        elif len(words) > 8:
            if words[4] != "PLR":
                return

            if '[' == words[6][0]:
                new_state = words[6].strip('[').strip(']')
            else:
                new_state = words[5].strip('[').strip(']')

        # check if state actually changed, otherwise no return statement is needed
        if self.state != new_state:
            self.state = new_state
            self.updated = True

            if self.state == 'Off':
                self.app = 'Off'
                self.close_signal = 'untagged'

    def update_app(self, words) -> None:
        # finds state name
        if '"normal":' in words:
            new_app = words[1] \
                .strip('"') \
                .split('http://eb.bluestacks.com/content_keymap/')[1] \
                .split('.cfg?')[0]

            if self.app != new_app:
                self.app = new_app
                self.updated = True

    def update_close_signal(self, words) -> None:
        if 'UI' in words:
            if 'onClosing' in words:
                self.close_signal = 'called'
                self.updated = True

    def get_update_methods(self):
        methods = inspect.getmembers(self, inspect.ismethod)
        updates = [method[0] for method in methods if method[0][:7] == 'update_']
        # updates = [method for method in a.__dir__() if method[:7] == 'update_']
        return updates
'''
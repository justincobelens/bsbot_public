from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Inputs(ABC):
    @property
    def phone(self):
        return

    def tap(self, x, y):
        self.phone.input_tap(x, y)

    def write(self, string):
        self.phone.input_text(string)

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from stepsimulation.utils.decorators import timer


@dataclass
class Navigate(ABC):
    app1: str = field(default='cz.webprovider.app1/.MainActivity')
    app2: str = field(default='com.app2.android/.mobile.main.ControlActivity')
    app3: str = field(default='io.github.blank.blank/.main.MainActivity')
    app4: str = field(default='com.app4/.MainActivity')

    def open_app(self, app):
        """ opens app and wait till it's done """
        try:
            package = self.__getattribute__(app)
        except AttributeError as e:
            # print(e)
            return

        self.phone.shell(f"am start -n {package}")

        if self.wait_app(app):
            return True
        else:
            return False

    def get_top_activity(self):
        activity = str(self.phone.get_top_activity()).split(' - ')[0]
        return activity

    timer(timeout=30, sleep=1)

    def wait_app(self, app) -> bool:
        if self.get_top_activity() == self.__getattribute__(app):
            return True

    @property
    def phone(self):
        return

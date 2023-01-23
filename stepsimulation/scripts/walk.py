import time
from dataclasses import dataclass, field

from stepsimulation.loop_all import loop
from stepsimulation.utils.decorators import timer
from stepsimulation.activity import Activity


@dataclass
class Walk:
    accounts: list
    current_set: int

    phone: any = field(init=False)

    activity: Activity = field(init=False)
    steps: int = field(init=False)
    pace: int = field(init=False)
    hours: int = field(init=False)
    minutes: int = field(init=False)

    def __post_init__(self):
        loop(self.script,
             self.accounts)

    def script(self, player):
        """ ----------------------------- START SCRIPT ----------------------------------- """
        error_msg = [True, 'no_error']
        self.phone = player.phone

        self.activity = Activity(player.number)

        self.steps = self.activity.daily_steps[self.current_set - 1]
        self.pace = self.activity.pace[self.current_set - 1]
        self.hours = self.activity.time[self.current_set - 1][0]
        self.minutes = self.activity.time[self.current_set - 1][1]

        print(f"Hours: {self.hours}, Minutes: {self.minutes}, Pace: {self.pace}")

        # open -blank-
        self.phone.open_app('-blank-')

        # set values in app
        self.set_hours()
        self.set_minutes()
        self.set_pace()
        self.review()

        # check registered
        registered = self.is_registered()
        if not registered:
            error_msg = [False, 'registry_error']
            return error_msg

        # print(registered)

        return error_msg

    @timer(timeout=60, sleep=1)
    def is_registered(self):
        return self.phone.dump_sync_app3()

    def review(self):
        self.phone.tap(480, 190)
        time.sleep(0.1)

        self.phone.tap(385, 625)
        time.sleep(0.1)

    def set_hours(self):
        self.phone.tap(177, 380)
        time.sleep(0.1)

        self.phone.write(self.hours)
        time.sleep(0.1)

        self.phone.tap(410, 540)
        time.sleep(0.1)

    def set_minutes(self):
        self.phone.tap(140, 440)
        time.sleep(0.1)

        self.phone.write(self.minutes)
        time.sleep(0.1)

        self.phone.tap(400, 540)
        time.sleep(0.1)

    def set_pace(self):
        min_px = 72
        max_px = 507

        pace_dx = ((max_px - min_px) / 100)
        pace_pxl = (self.pace - 100) * pace_dx + min_px

        self.phone.tap(pace_pxl, 516)
        time.sleep(0.1)

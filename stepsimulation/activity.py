import random
import numpy as np

from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Activity:
    number: str

    date: datetime = field(default=datetime.now())

    min_steps: int = field(default=22_000)
    max_steps: int = field(default=28_000)
    min_pace: int = field(default=100)
    max_pace: int = field(default=135)
    total_sets: int = field(default=4)

    pace: list = field(default_factory=list)
    time: list = field(default_factory=list)

    seed: int = field(init=False)
    daily_steps: list = field(init=False)
    total_steps: int = field(init=False)

    def __post_init__(self):
        date_corrected = self.date - timedelta(hours=16)

        self.seed = int(date_corrected.strftime('%Y%m%d')) + int(self.number)

        np.random.seed(self.seed)
        random.seed(self.seed)

        self.calc_total_steps()
        self.calc_daily_steps()
        self.calc_pace()
        self.calc_time()

    def calc_total_steps(self):
        self.total_steps = random.randint(self.min_steps, self.max_steps)

    def calc_daily_steps(self):
        mu = self.total_steps / self.total_sets
        sigma = mu / self.total_sets

        for i in range(self.total_sets):
            new_sets = np.random.normal(mu, sigma, self.total_sets)
            # new_sets = np.random.poisson(mu, self.total_sets)
            self.daily_steps = list(map(round, new_sets))

            if abs(self.total_steps - sum(new_sets)) < 1000:
                break

    def calc_pace(self):
        self.pace = random.sample(range(self.min_pace, self.max_pace), len(self.daily_steps))

    def calc_time(self):
        time_list = []
        for i, new_set in enumerate(self.daily_steps):
            total_minutes = round(new_set / self.pace[i]) - 1

            minutes = total_minutes % 60
            hours = round((total_minutes - minutes) / 60)

            time_list.append([hours, minutes])

        self.time = time_list


# old
'''
import json
import os

import date

DIRECTORY_BASE = fr'activities'


def create_directory(account, overwrite=False):
    # Create Directory
    directory = fr'{DIRECTORY_BASE}/{account}'

    # Creates File
    filename = fr"{directory}/{account}.json"

    # Create target directory & all intermediate directories if don't exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("- Directory ", directory, " Created ")

    # Check if account already exist
    if os.path.exists(filename):
        with open(filename) as json_file_read:
            data = json.load(json_file_read)
            timestamp = data["timestamp"]
    else:
        timestamp = ""

    if not overwrite:
        # Check if already updated
        if timestamp == date.today().strftime("%Y%m%d"):
            print(account, "is already up to date for this week")
            return


def save_activity(account, week):
    # Create Directory
    directory = fr'{DIRECTORY_BASE}/{account}'

    # Creates File
    filename = fr"{directory}/{account}.json"

    # write activities to disk
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(week.data, f, indent=4)
        print(f"Updated: {account} ")


@dataclass
class Week:
    monday: tuple = field(default_factory=tuple)
    tuesday: tuple = field(default_factory=tuple)
    wednesday: tuple = field(default_factory=tuple)
    thursday: tuple = field(default_factory=tuple)
    friday: tuple = field(default_factory=tuple)
    saturday: tuple = field(default_factory=tuple)
    sunday: tuple = field(default_factory=tuple)

    timestamp: date = field(default=date.today().strftime("%Y%m%d"))

    def __post_init__(self):
        # Structure of data
        self.data = {"timestamp": self.timestamp,
                     "dailySteps": {
                         "monday": self.monday,
                         "tuesday": self.tuesday,
                         "wednesday": self.wednesday,
                         "thursday": self.thursday,
                         "friday": self.friday,
                         "saturday": self.saturday,
                         "sunday": self.sunday
                     }}

    def update(self, day, daily_steps, time, pace):
        for i, new_set in enumerate(daily_steps):
            hours = time[i][0]
            minutes = time[i][1]

            temp = {"set" + str(i + 1):
                        {"steps": daily_steps[i],
                         "pace": pace[i],
                         "time": {"hours": hours,
                                  "minutes": minutes
                                  }
                         }
                    }

            if i == 0:
                self.data["dailySteps"][day] = temp
            else:
                self.data["dailySteps"][day].update(temp)


@dataclass()
class Activity:
    total_sets: int = field(default=4)
    min_steps: int = field(default=22_000)
    max_steps: int = field(default=28_000)
    daily_steps: list = field(init=False)

    min_pace: int = field(default=100)
    max_pace: int = field(default=135)
    pace: list = field(init=False)

    time: list = field(init=False)

    def __post_init__(self):
        self.total_steps = random.randint(self.min_steps, self.max_steps)

    def calc_steps(self):
        mu = self.total_steps / self.total_sets
        sigma = mu / self.total_sets

        ratios = [2.7]

        for i in range(self.total_sets):
            new_sets = np.random.normal(mu, sigma, self.total_sets)
            # new_sets = np.random.poisson(mu, self.total_sets)
            self.daily_steps = list(map(round, new_sets))

            if abs(self.total_steps - sum(new_sets)) < 1000:
                break

    def calc_pace(self):
        self.pace = random.sample(range(self.min_pace, self.max_pace), len(self.daily_steps))

    def calc_time(self):
        time_list = []
        for i, new_set in enumerate(self.daily_steps):
            total_minutes = round(new_set / self.pace[i]) - 1

            minutes = total_minutes % 60
            hours = round((total_minutes - minutes) / 60)

            time_list.append([hours, minutes])

        self.time = time_list


def update_accounts(accounts, total_sets, force_update=False):
    for account in accounts:
        print(f"\nRunning... {account}")

        # create dir
        if create_directory(account, overwrite=force_update) is not None:
            continue

        # create activity dataclass
        week = Week()
        activity = Activity(total_sets=total_sets)

        days = week.data["dailySteps"]

        for day in days:
            # calculates the total amount of steps per set
            activity.calc_steps()

            # calculates the pace per set
            activity.calc_pace()

            # calculates the time per set
            activity.calc_time()

            daily_steps = activity.daily_steps
            time = activity.time
            pace = activity.pace

            week.update(day, daily_steps, time, pace)

        save_activity(account, week)
'''

'''import os
import time
import json
from dataclasses import replace

from .player import Player


def follow(file):
    file.seek(0, os.SEEK_END)
    while True:
        try:
            line = file.readline()
        except UnicodeError as e:
            print(e)
            line = str(e)

        if not line:
            time.sleep(0.1)
            continue

        if '[GUEST]:' in line.split():
            continue
        yield line


def upload(data):
    filename = fr'core/listener/player_info/player.json'

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def listen():
    log_path = r"D:\Bluestacks Engines\BlueStacks_nxt\Logs\Player.log"
    log_file = open(log_path, 'r', encoding='cp437')
    log_lines = follow(log_file)

    # create phone
    phone = Player(number=0, state='Off', app='Off', close_signal='untagged')
    upload(phone.dict())

    # read lines for updates
    for line in log_lines:
        updates = phone.get_update_methods()

        # loop through update methods
        for fn in updates:
            # evaluates the object method: phone.method(arg)
            eval(f"phone.{fn}({line.split()})")

            if phone.updated:
                phone = replace(phone, updated=False)
                upload(phone.dict())
                continue


if __name__ == "__main__":
    listen()
'''
import subprocess

from dataclasses import dataclass, field
from ppadb.client import Client as AdbClient

from plugins.phone.hotkeys import Hotkeys
from plugins.phone.inputs import Inputs
from plugins.phone.ip import Ip
from plugins.phone.navigate import Navigate
from plugins.phone.adb_port import adb_port
from plugins.phone.dump import UIDump

from utils.decorators import timer


@dataclass
class Phone(Hotkeys, Inputs, Navigate, Ip, UIDump):
    client: AdbClient = field(default=AdbClient())
    phone: AdbClient.device = field(default=None)

    app: str = field(init=False)
    ip: str = field(init=False)

    port: str = field(init=False)
    serial: str = field(init=False)

    def connect(self, number: str):
        self.serial = f"localhost:{adb_port(number)}"

        result = subprocess.run(["adb", "connect", f"{self.serial}"], capture_output=True, text=True)
        # print(result)

        devices = AdbClient().devices()
        if len(devices) == 0:
            print("no devices attached")
            return None

        self.phone = self.client.device(self.serial)

    @timer(timeout=30, sleep=1)
    def is_connected(self, number: str) -> bool:
        state = subprocess.run(["adb", 'get-state'], capture_output=True, text=True)
        if state.stdout.strip() == 'device':
            return True

        elif state.stderr.strip() == r'error: no devices/emulators found':
            self.connect(number)
            return False

    @timer(timeout=30, sleep=1)
    def is_ready(self) -> bool:
        top_activity = self.phone.get_top_activity()
        if top_activity:
            return True
        else:
            return False

    def disconnect(self):
        result = subprocess.run(["adb", "disconnect", f"{self.serial}"], capture_output=True, text=True)
        # print(result)

    @staticmethod
    def disconnect_all():
        AdbClient().remote_disconnect()

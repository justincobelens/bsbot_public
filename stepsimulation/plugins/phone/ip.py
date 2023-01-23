import subprocess

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from stepsimulation.utils.decorators import timer


@dataclass
class Ip(ABC):

    @timer(timeout=60, sleep=1)
    def check_ip(self):
        result = subprocess.run(["adb", "exec-out",
                                 'host', 'myip.opendns.com', 'resolver1.opendns.com'],
                                capture_output=True, text=True)

        myip_response = result.stdout.strip().split(' ')[-1]
        ip = myip_response

        if not ip:
            # print(f"no ip: {result}")
            return

        if ip == 'found.':
            print('no internet access')
            return
        if ip[0].isdigit():
            if ip != "-blank-":
                return ip
        else:
            # print(f"no digit : {result}")
            return
        return

    @property
    def phone(self):
        return self.phone()

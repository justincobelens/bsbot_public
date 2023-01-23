import subprocess
from dataclasses import dataclass, field


@dataclass
class Server:
    server_active: bool = field(init=False, default=False)

    @staticmethod
    def _execute_command(cmd, with_response=True):
        result = subprocess.run(["adb", f"{cmd}"], capture_output=with_response, text=True)
        if with_response:
            return result

    def start_server(self):
        cmd = 'start-server'
        # print('Starting adb - server')
        result = self._execute_command(cmd)
        # print(result)

        # TODO
        # add if tree to check if server started
        self.server_active = True

    def stop_server(self):
        cmd = 'kill-server'
        # print('Stopping adb - server')
        result = self._execute_command(cmd)
        # print(result)

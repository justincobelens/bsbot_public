import subprocess

from dataclasses import dataclass


@dataclass
class UIDump:
    @staticmethod
    def dumpsys():
        result = subprocess.run(["adb", "exec-out", 'uiautomator', 'dump', '/dev/tty'],
                                capture_output=True, text=True)

        if result:
            dump = result.stdout.split('node')
            return dump

    def dump_app2(self):
        dump = self.dumpsys()

        for ele in dump:
            if ele[1:10] == 'index="1"':
                if 'resource-id="com.app2.android:id/status_bar_root_container' in ele:
                    connection = ele.split('" ')[1].split('"')[1]
                    return connection
        return None

    def dump_google_fit(self):
        dump = self.dumpsys()
        for ele in dump:
            if ele[1:10] == 'index="6"':
                ele2 = ele.split(' ')
                if ele2[3] == 'resource-id="com.google.android.apps.fitness:id/halo_step_label"':
                    steps = ele2[2].split('"')[1]
                    return steps
        return None

    def dump_steps_app4(self):
        dump = self.dumpsys()

        for ele in dump:
            if ele[1:10] == 'index="2"':
                ele2 = ele.split(' ')
                if ele2[2] == 'text="Steps:':
                    steps = ele2[3].strip('"')
                    return steps
        return None

    def dump_ads_app4(self):
        dump = self.dumpsys()

        for ele in dump:
            if ele[1:10] == 'index="1"':
                mp = ele.split('" ')[1]
                if 'text="Your next rewards will now be' in mp:
                    current_mp = mp.split(' ')[-2].strip('%')
                    return current_mp

    def dump_sync_app3(self):
        dump = self.dumpsys()

        for ele in dump:
            if ele[1:10] != 'index="2"':
                continue

            if 'resource-id="io.github.blank.blank:id/button_summary"' not in ele:
                continue

            current_runs = ele.split('" ')[1].split('"')[1]
            if current_runs == "No active runs":
                return

            return current_runs
        return False

    def dump_ads(self):
        dump = self.dumpsys()

        for ele in dump:
            if ele[1:10] == 'index="0"':
                ele2 = ele.split('" ')

                if 'text="Reward granted' in ele2:
                    reward_granted = ele2[1].split('"')[1]
                    return reward_granted

                if ele2[1][0:5] == 'text=':
                    if ele2[1].split(' ')[-1] == "remaining":
                        seconds_remaining = ele2[1].split('"')[0:][-1]
                        return seconds_remaining


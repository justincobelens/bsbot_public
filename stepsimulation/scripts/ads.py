import time
from dataclasses import dataclass, field

from stepsimulation.loop_all import loop
from stepsimulation.utils.decorators import timer


@dataclass
class Ads:
    accounts: list
    phone: any = field(init=False)

    max_ads_mp: float
    steps: int = field(default=0)
    ads_mp: float = field(default=0.0)

    def __post_init__(self):
        loop(self.script,
             self.accounts)

    def script(self, player):
        """ ----------------------------- START SCRIPT ----------------------------------- """
        error_msg = [True, 'no_error']
        self.phone = player.phone

        self.phone.open_app('-blank-')

        while True:
            if not self.is_synced():
                error_msg = [False, 'ad_sync_error']
                return error_msg

            print(f"Steps  : {self.steps}")
            print(f"Ads mp : {self.ads_mp}")

            if self.ads_mp < self.max_ads_mp:
                # run ad
                if not self.load_ad():
                    error_msg = [False, 'ad_loading_error']
                    return error_msg

                # wait for ad to finish
                if not self.is_ad_finished():
                    error_msg = [False, 'ad_finishing_error']
                    return error_msg

                self.phone.home()
                time.sleep(1)

                self.phone.open_app('-blank-')

                # print ads multiplier
                self.ads_mp = float(self.phone.dump_ads_app4())
            else:
                break

        return error_msg

    @timer(timeout=120, sleep=1)
    def is_synced(self) -> bool:
        dump_steps = self.phone.dump_steps_app4()
        if dump_steps:
            self.steps = int(dump_steps)
            self.ads_mp = float(self.phone.dump_ads_app4())
            return True
        else:
            return False

    def get_activity(self) -> str:
        activity = str(self.phone.get_top_activity()).split(' - ')[0]

        activities = {
            '-blank-_home': 'com.-blank-/.MainActivity',
            'ads_running': 'com.-blank-/com.google.android.gms.ads.AdActivity',
            'ads_after': 'com.-blank-/com.google.android.finsky.activities.MarketDeepLinkHandlerActivity'
        }

        if activity in activities.values():
            key = list(activities.keys())[list(activities.values()).index(activity)]
            return key

    @timer(timeout=60, sleep=5)
    def load_ad(self) -> bool:
        activity = self.get_activity()

        if activity == '-blank-_home':
            # click logo to load ad
            self.phone.tap(66, 76)
            return False

        elif activity == 'ads_running' or activity == 'ads_after':
            return True

    @timer(timeout=60, sleep=1)
    def is_ad_finished(self) -> bool:
        # check if still running
        activity = self.get_activity()
        dump_ads = self.phone.dump_ads()

        # check if activity changed or rewarded granted msg appeared
        if activity == 'ads_after' or dump_ads == 'Reward granted':
            return True

        elif activity == 'ads_running':
            return False

        elif dump_ads:
            print('dump ads error')
            print(dump_ads)

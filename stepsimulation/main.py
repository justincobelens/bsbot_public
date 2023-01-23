import time
import random
import multiprocessing as mp

from scripts.walk import Walk
from scripts.ads import Ads

from utils.get_accounts import get_account_from_file


def active_scripts(accounts):
    # session 1
    Walk(accounts=accounts, current_set=1)
    Ads(accounts=accounts, max_ads_mp=10)

    # session 2
    time.sleep(random.randint(80, 110) * 60)
    Walk(accounts=accounts, current_set=2)
    Ads(accounts=accounts, max_ads_mp=15)

    # session 3
    time.sleep(random.randint(80, 110) * 60)
    Walk(accounts=accounts, current_set=3)
    Ads(accounts=accounts, max_ads_mp=20)

    # session 4
    time.sleep(random.randint(80, 110) * 60)
    Walk(accounts=accounts, current_set=4)
    Ads(accounts=accounts, max_ads_mp=25)


def main():
    # get accounts
    accounts = get_account_from_file()

    # start bluestacks, adb-server and run scripts
    simulating = mp.Process(target=active_scripts, args=(accounts,))

    # start multiprocessing
    simulating.start()

    # wait till simulating is done
    simulating.join()

    # stop all processes
    # listening.terminate()


if __name__ == "__main__":
    main()

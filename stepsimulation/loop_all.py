from datetime import datetime

from player import Player
from core.server import Server


def loop(script, accounts_list: list[list[str]]):
    # start adb-server
    server = Server()
    server.stop_server()
    server.start_server()

    skipped = []

    # loop over accounts with script
    for i, account in enumerate(accounts_list):

        player = Player(number=account[0],
                        name=account[1])

        # start new player
        start, error = player.start()
        if not start:
            player.stop()
            skipped.append([account[0], error])
            continue

        # check vpn connection, by checking ip-address and app2 app
        player.phone.open_app('app2')

        ip = player.phone.check_ip()
        if not ip:
            player.stop()
            skipped.append([account[0], 'vpn_error'])
            continue

        player.phone.open_app('app2')
        vpn_server = player.phone.dump_app2()

        print(vpn_server)
        print(f"IP Address: {ip}")

        # run script
        script_result, error = script(player)
        if not script_result:
            player.stop()
            skipped.append([account[0], error])
            continue

        # print(datetime.now())
        player.stop()

    # stop adb-server
    server.stop_server()
    print(skipped)

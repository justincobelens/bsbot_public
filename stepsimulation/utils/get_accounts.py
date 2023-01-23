import os


def get_account_from_file() -> list[list[str]]:
    accounts = []
    filename = os.path.join(os.path.dirname(__file__), os.pardir, 'accounts_rawdata')

    with open(filename) as f:
        for line in f:
            part = line.split("\t")

            number = part[0]
            name = part[1]
            address = part[2].rstrip()

            account = [number, name, address]
            accounts.append(account)
    return accounts

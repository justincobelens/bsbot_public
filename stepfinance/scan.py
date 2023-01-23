from utils import *
from bscscan import Bscscan

API_KEY = input("API Key: ")
look_up_date = input('Lookup date(YYYY-MM-DD): ')

POOL_ADDRESS = "0x0000000000000000000000000000000000000000"
CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"


def main():
    print(f"Getting rewards for {look_up_date}")

    b = Bscscan(key=API_KEY)
    start_block_number, end_block_number = get_block_numbers(b, look_up_date)

    # getting token transfers
    # txs_contract = b.get_transactions(CONTRACT_ADDRESS, start_block_number, end_block_number)

    # correcting token balance from today with balance given date
    # timestamps = []
    # addresses = []
    # values = []
    # for tx in txs_contract:
    #     if tx['functionName'][:8] == 'transfer':
    #         print(tx)
    #     timestamp, address, value = get_contract_transfer_addresses_values(tx)
    #     timestamps.append(timestamp)
    #     addresses.append(address)
    #     values.append(value)

    print("Calculating balances at payout")

    # getting transactions
    txs_pool = b.get_transactions(POOL_ADDRESS, start_block_number, end_block_number)

    # correcting BNB balance from today with balance given date
    users = []
    for tx in txs_pool:
        addresses, rewards = get_pool_rewarded_addresses_rewards(tx)

        balances = \
            list(
                map(lambda address:
                    corrected_token_balance_to_timestamp(b,
                                                         CONTRACT_ADDRESS,
                                                         address,
                                                         start_block_number,
                                                         end_block_number),
                    addresses))

        users.extend(list(zip(addresses, balances, rewards)))


if __name__ == "__main__":
    main()

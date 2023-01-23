import time

from datetime import datetime, timedelta


def get_block_numbers(bsc, date):
    from_date = datetime.strptime(date, "%Y-%m-%d")
    to_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(hours=24)

    from_timestamp = from_date.timestamp()
    to_timestamp = to_date.timestamp()

    start_block_number = bsc.get_block_number_by_timestamp(int(from_timestamp))
    end_block_number = bsc.get_block_number_by_timestamp(int(to_timestamp))

    if not start_block_number.isdigit():
        print('Give valid start date')
        quit()

    if not end_block_number.isdigit():
        print('End time given is in the future, changing to last block')

        end_block_number = bsc.get_block_number_by_timestamp('latest')
        if int(end_block_number) < int(start_block_number):
            print('Something went wrong calculating blocks')

    return start_block_number, end_block_number


def get_contract_transfer_addresses_values(tx):
    function_name = tx['functionName']
    block_number = tx['blockNumber']
    timestamp = tx['timeStamp']
    from_address = tx['from']
    to_address = tx['to']
    value = tx['value']

    return timestamp, to_address, value


def get_pool_rewarded_addresses_rewards(tx):
    """
    Returns list of tuples (address, reward in wei)
    """
    tx_input = tx["input"]

    lines = tx_input[10:].split("0000000000000000000000000000000000000000000000000000000000000032")  # 64 digits

    raw_addresses = list(map(''.join, zip(*[iter(lines[1:][0])] * 64)))
    raw_values = list(map(''.join, zip(*[iter(lines[2:][0])] * 64)))

    addresses = list(map(lambda x: f"0x{x[24:]}", raw_addresses))  # add 0x in front of raw_addresses
    values = list(map(lambda x: int(x[24:], base=16), raw_values))  # convert hex to int

    return addresses, values


def get_timestamp(tx):
    return datetime.fromtimestamp(int(tx["timeStamp"]))


def get_token_balance(Bsc, address):
    return int(Bsc.get_balance(address))


def corrected_token_balance_to_timestamp(Bsc, contract_address, address, start_block, end_block):
    """
    Returns balance(wei) corrected to given timestamp
    """

    start = time.time()
    events = Bsc.get_token_transfer_events(contract_address=contract_address,
                                           address=address,
                                           start_block=start_block,
                                           end_block=end_block)

    balance = get_token_balance(Bsc, address)

    if len(events) == 0:
        return balance

    for event in events:
        timestamp = datetime.fromtimestamp(int(event['timeStamp']))
        today = f"{datetime.now().strftime('%Y-%m-%d')} 16:00:00"

        if timestamp > datetime.strptime(today, "%Y-%m-%d %H:%M:%S"):
            value = int(event["value"])
            if event["from"] == address:
                balance += value
            elif event["to"] == address:
                balance -= value
    print(f"Correct: {time.time() - start}")
    print("=============")

    return balance

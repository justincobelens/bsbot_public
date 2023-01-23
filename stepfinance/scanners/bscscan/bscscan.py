from dataclasses import dataclass, field
from requests import get


@dataclass
class Bscscan:
    url: str = field(init=False)
    key: str = field(default="")

    def make_api_url(self, module, action, **kwargs):
        """
        Returns api url for www.bscscan.com/api
        """

        base_url = "https://api.bscscan.com/api"

        self.url = base_url + f"?module={module}&action={action}&apikey={self.key}"

        for key, value in kwargs.items():
            self.url += f"&{key}={value}"

        return self.url


@dataclass
class Accounts(Bscscan):
    def get_balance(self, address):
        """
        Returns the BNB balance of a given address.
        """

        url = self.make_api_url("account", "balance", address=address)

        response = get(url)
        return response.json()["result"]

    def get_balance_multiple(self, address_list):
        """
        Returns the balance of the accounts from a list of addresses.
        """

        if len(address_list) == 0:
            raise ValueError("Address list is empty")

        if len(address_list) > 20:
            raise ValueError("Address list can't contain more than 20 addresses")

        addresses = ""
        for address in address_list:
            if addresses == "":
                addresses = f"{address}"
            else:
                addresses = f"{addresses}, {address}"

        url = self.make_api_url("account", "balancemulti",
                                address=addresses, tag='latest')

        response = get(url)
        return response.json()["result"]

    def get_transactions(self, address, start_block, end_block):
        """
        Returns the list of transactions performed by an address, with optional pagination.
        """

        url = self.make_api_url("account", "txlist",
                                address=address, startblock=start_block, endblock=end_block,
                                page=1, offset=10000, sort="asc")

        response = get(url)
        return response.json()["result"]

    def get_internal_txs(self, address, start_block, end_block):
        """
        Returns the list of internal transactions performed by an address, with optional pagination.
        """

        url = self.make_api_url("account", "txlistinternal",
                                address=address, startblock=start_block, endblock=end_block,
                                page=1, offset=10000, sort="asc")

        response = get(url)
        return response.json()["result"]

    def get_token_transfer_events(self, contract_address, address, start_block, end_block):
        """
        Returns the list of BEP-20 tokens transferred by an address, with optional filtering by token contract.
        """

        url = self.make_api_url("account", "tokentx", contractaddress=contract_address,
                                address=address, startblock=start_block, endblock=end_block,
                                page=1, offset=10000, sort="asc")

        response = get(url)
        return response.json()["result"]


@dataclass
class Contracts(Bscscan):

    def get_abi(self, contract_address):
        """
        Returns the contract Application Binary Interface ( ABI ) of a verified smart contract.
        https://api.bscscan.com/api
        """

        url = self.make_api_url("contract", "getabi",
                                address=contract_address)

        response = get(url)
        return response.json()["result"]


@dataclass
class Blocks(Bscscan):

    def get_block_number_by_timestamp(self, timestamp):
        """
        Returns the block number that was validated at a certain timestamp.
        """
        url = self.make_api_url("block", "getblocknobytime",
                                timestamp=timestamp, closest="before")

        response = get(url)
        return response.json()["result"]


@dataclass
class Logs(Bscscan):

    def get_log(self, from_block, to_block, address, topic0):
        """
        Returns the block number that was validated at a certain timestamp.
        """
        url = self.make_api_url("logs", "getLogs",
                                fromBlock=from_block, toBlock=to_block, address=address,
                                topic0=topic0)

        response = get(url)
        return response.json()["result"]


@dataclass
class Proxy(Bscscan):

    def get_block(self, block_number):
        """
        Returns information about a block by block number.
        """
        url = self.make_api_url("proxy", "eth_getBlockByNumber",
                                tag=hex(block_number), boolean="true")

        response = get(url)
        return response.json()["result"]

    def get_transaction_by_hash(self, txhash):
        """
        Returns information about a transaction requested by transaction hash.
        """

        url = self.make_api_url("proxy", "eth_getTransactionByHash",
                                txhash=txhash, )

        response = get(url)
        return response.json()["result"]

    def get_transaction_count(self, address):
        """
        Returns the number of transactions performed by an address.
        """

        url = self.make_api_url("proxy", "eth_getTransactionCount",
                                address=address, tag='latest')

        response = get(url)
        return int(response.json()["result"], base=16)


@dataclass
class Tokens(Bscscan):

    def get_token_balance_by_contract(self, address, contract_address):
        """
        Returns the current balance of a BEP-20 token of an address.
        """

        url = self.make_api_url("account", "tokenbalance",
                                contractaddress=contract_address, address=address,
                                tag="latest")

        response = get(url)
        return response.json()["result"]


@dataclass
class Stats(Bscscan):
    def get_bnb_price(self):
        """
        Returns the latest price of 1 BNB.
        """

        url = self.make_api_url("stats", "bnbprice")

        response = get(url)
        return response.json()["result"]



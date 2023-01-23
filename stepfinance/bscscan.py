from dataclasses import dataclass, field
from scanners.bscscan.bscscan import *

@dataclass
class Bscscan(Accounts, Contracts, Blocks, Proxy, Tokens, Stats):
    pass

from enum import Enum

class TxType(str, Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"
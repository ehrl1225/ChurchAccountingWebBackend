from pydantic import BaseModel

from common.enum.tx_type import TxType


class CategoryCheck(BaseModel):
    name: str
    tx_type:TxType
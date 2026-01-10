from pydantic import BaseModel

from common.database import TxType


class CategoryCheck(BaseModel):
    name: str
    tx_type:TxType
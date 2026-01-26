from pydantic import BaseModel

from common.enum.tx_type import TxType


class ItemCheck(BaseModel):
    category_name: str
    tx_type: TxType
    item_name: str

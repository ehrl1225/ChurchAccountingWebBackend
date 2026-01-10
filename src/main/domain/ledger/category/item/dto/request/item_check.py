from pydantic import BaseModel

from common.database import TxType


class ItemCheck(BaseModel):
    category_name: str
    tx_type: TxType
    item_name: str

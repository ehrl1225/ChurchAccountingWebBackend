from pydantic import BaseModel
from datetime import date

from common.database import TxType


class EditReceiptDto(BaseModel):
    receipt_id: int
    receipt_image_url: str
    paper_date: date
    actual_date: date
    name: str
    tx_type: TxType
    amount: int
    category_id: int
    item_id: int
    event_id: int
    etc:str
from typing import Optional

from pydantic import BaseModel
from datetime import date

from common.database import TxType


class CreateReceiptDto(BaseModel):
    receipt_image_id: Optional[int]
    paper_date: date
    actual_date: Optional[date]
    name: str
    tx_type: TxType
    amount: int
    category_id: int
    item_id: int
    event_id: Optional[int]
    etc: Optional[str]
    organization_id: int
    year:int
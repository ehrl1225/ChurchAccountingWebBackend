from typing import Optional

from pydantic import BaseModel
from datetime import date

from common.database import TxType


class EditReceiptDto(BaseModel):
    organization_id: int
    receipt_id: int
    receipt_image_url: Optional[str]
    paper_date: date
    actual_date: Optional[date]
    name: str
    tx_type: TxType
    amount: int
    category_id: int
    item_id: int
    event_id: Optional[int]
    etc:Optional[str]
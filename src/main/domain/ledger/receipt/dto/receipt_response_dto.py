from typing import Optional

from pydantic import BaseModel
from datetime import date

from common.database import TxType


class ReceiptResponseDto(BaseModel):
    id : int
    receipt_image_url: str
    paper_date: date
    actual_date: Optional[date]
    name: str
    tx_type: TxType
    amount: int
    category_id: int
    category_name: str
    item_id: int
    item_name: str
    etc: Optional[str]
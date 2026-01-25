from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date

from common.enum.tx_type import TxType


class ReceiptResponseDto(BaseModel):
    id : int
    receipt_image_id: Optional[int] = None
    receipt_image_file_name: Optional[str] = None
    paper_date: date
    actual_date: Optional[date] = None
    name: str
    tx_type: TxType
    amount: int
    category_id: int
    category_name: Optional[str] = None
    item_id: int
    item_name: Optional[str] = None
    event_id: Optional[int]
    event_name: Optional[str] = None
    etc: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
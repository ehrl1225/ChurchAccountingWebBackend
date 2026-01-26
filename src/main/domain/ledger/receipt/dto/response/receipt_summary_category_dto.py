from pydantic import BaseModel

from common.enum.tx_type import TxType
from domain.ledger.receipt.dto.response.receipt_summary_item_dto import ReceiptSummaryItemDto


class ReceiptSummaryCategoryDto(BaseModel):
    category_id: int
    category_name: str
    tx_type: TxType
    amount: int
    items: list[ReceiptSummaryItemDto]
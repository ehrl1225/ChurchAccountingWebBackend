from pydantic import BaseModel

from domain.ledger.receipt.dto.response.receipt_summary_item_dto import ReceiptSummaryItemDto


class ReceiptSummaryCategoryDto(BaseModel):
    category_name: str
    amount: int
    items: list[ReceiptSummaryItemDto]
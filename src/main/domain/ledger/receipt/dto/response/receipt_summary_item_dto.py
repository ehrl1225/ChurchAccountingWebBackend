from pydantic import BaseModel

class ReceiptSummaryItemDto(BaseModel):
    item_name: str
    amount: int
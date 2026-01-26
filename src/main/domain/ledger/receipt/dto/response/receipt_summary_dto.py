from typing import Optional

from pydantic import BaseModel

from domain.ledger.receipt.dto.response.receipt_summary_category_dto import ReceiptSummaryCategoryDto
from common.enum.summary_type import SummaryType


class ReceiptSummaryDto(BaseModel):
    summary_type: SummaryType
    month_number: Optional[int] = None
    event_id: Optional[int] = None
    event_name: Optional[str] = None
    total_income: int
    total_outcome: int
    balance: int
    categories: list[ReceiptSummaryCategoryDto]
    carry_amount: Optional[int] = None
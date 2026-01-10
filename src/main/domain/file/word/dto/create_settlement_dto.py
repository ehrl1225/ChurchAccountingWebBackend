from typing import Optional

from pydantic import BaseModel

from domain.ledger.receipt.dto import SummaryType


class CreateSettlementDto(BaseModel):
    summary_type: SummaryType
    month_number: Optional[int]
    event_id: Optional[int]
    organization_id: int
    year: int
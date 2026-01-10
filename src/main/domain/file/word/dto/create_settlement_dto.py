from typing import Optional

from domain.ledger.receipt.dto import SummaryType
from fastapi import Query

class CreateSettlementDto:
    summary_type: SummaryType
    month_number: Optional[int]
    event_id: Optional[int]
    organization_id: int
    year: int

    def __init__(
            self,
            summary_type: SummaryType = Query(SummaryType.MONTH),
            month_number: Optional[int] = Query(None),
            event_id: Optional[int] = Query(None),
            organization_id: Optional[int] = Query(),
            year: Optional[int] = Query(),
    ):
        self.summary_type = summary_type
        self.month_number = month_number
        self.event_id = event_id
        self.organization_id = organization_id
        self.year = year
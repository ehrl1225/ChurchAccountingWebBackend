from typing import Optional
from fastapi import Query

from domain.ledger.receipt.dto.summary_type import SummaryType


class ReceiptSummaryParams:
    summary_type:SummaryType
    month_number: Optional[int]
    event_id:Optional[int]
    organization_id: int
    year: int

    def __init__(
            self,
            summary_type: SummaryType = Query(description="Summary Type"),
            month_number: Optional[int] = Query(None, description="Month"),
            event_id: Optional[int] = Query(None, description="Event ID"),
            organization_id: int = Query(description="Organization ID"),
            year: int = Query(description="Year"),
    ):
        self.summary_type = summary_type
        self.month_number = month_number
        self.event_id = event_id
        self.organization_id = organization_id
        self.year = year
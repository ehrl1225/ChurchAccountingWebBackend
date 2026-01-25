from typing import Optional
from pydantic import BaseModel

from common.enum.summary_type import SummaryType


class DownloadReceiptImageDto(BaseModel):
    organization_id: int
    year: int
    summary_type: SummaryType
    month: Optional[int]
    event_id: Optional[int]
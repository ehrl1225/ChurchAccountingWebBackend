from typing import Optional

from fastapi import Query
from common.enum.tx_type import TxType


class SearchCategoryParams:
    organization_id:int
    year:int
    tx_type:Optional[TxType]

    def __init__(
            self,
            organization_id: int = Query(description="Organization ID"),
            year: int = Query( description="Year"),
            tx_type: Optional[TxType] = Query(None, description="Transaction Type"),
    ):
        self.organization_id = organization_id
        self.year = year
        self.tx_type = tx_type

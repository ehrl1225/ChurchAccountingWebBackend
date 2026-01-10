from fastapi import Query
from common.database import TxType


class SearchCategoryParams:
    organization_id:int
    year:int
    tx_type:TxType

    def __init__(
            self,
            organization_id: int|None = Query(description="Organization ID"),
            year: int|None = Query(description="Year"),
            tx_type: TxType = Query(description="Transaction Type"),
    ):
        self.organization_id = organization_id
        self.year = year
        self.tx_type = tx_type

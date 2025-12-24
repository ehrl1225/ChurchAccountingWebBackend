from pydantic import BaseModel

from common.database import TxType


class SearchCategoryDto(BaseModel):
    organization_id:int
    year:int
    tx_type:TxType
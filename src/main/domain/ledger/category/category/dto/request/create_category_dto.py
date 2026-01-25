from pydantic import BaseModel

from common.enum.tx_type import TxType


class CreateCategoryDTO(BaseModel):
    category_name: str
    item_name: str | None
    tx_type: TxType
    organization_id: int
    year: int
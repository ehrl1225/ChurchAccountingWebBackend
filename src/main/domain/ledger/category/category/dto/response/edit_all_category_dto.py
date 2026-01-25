from typing import Optional

from pydantic import BaseModel

from common.enum.tx_type import TxType
from domain.ledger.category.item.dto import EditAllItemDto


class EditAllCategoryDto(BaseModel):
    id: Optional[int]
    name: str
    tx_type: TxType
    items: list[EditAllItemDto]
    deleted: bool


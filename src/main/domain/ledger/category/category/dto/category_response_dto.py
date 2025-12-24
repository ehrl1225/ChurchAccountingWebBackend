from pydantic import BaseModel

from common.database import TxType
from domain.ledger.category.item.dto.item_response_dto import ItemResponseDto


class CategoryResponseDto(BaseModel):
    id: int
    name: str
    items: list[ItemResponseDto]
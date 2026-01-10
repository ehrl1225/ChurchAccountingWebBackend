from pydantic import BaseModel, ConfigDict

from common.database import TxType
from domain.ledger.category.item.dto.response.item_response_dto import ItemResponseDto


class CategoryResponseDto(BaseModel):
    id: int
    name: str
    tx_type: TxType
    items: list[ItemResponseDto] = []

    model_config = ConfigDict(from_attributes=True)
from typing import Optional

from pydantic import BaseModel

from domain.ledger.category.item.dto import EditAllItemDto


class EditAllCategoryDto(BaseModel):
    organization_id: int
    year: int
    id: Optional[int]
    name: str
    items: list[EditAllItemDto]
    deleted: bool


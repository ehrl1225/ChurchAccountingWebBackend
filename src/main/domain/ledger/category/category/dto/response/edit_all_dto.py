from pydantic import BaseModel

from domain.ledger.category.category.dto.response import EditAllCategoryDto


class EditAllDto(BaseModel):
    organization_id: int
    year: int
    categories: list[EditAllCategoryDto]

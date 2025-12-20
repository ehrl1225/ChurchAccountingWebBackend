from pydantic import BaseModel

class CreateItemDto(BaseModel):
    category_id: int
    item_name: str
    organization_id: int
    year: int
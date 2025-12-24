from pydantic import BaseModel

class EditItemDto(BaseModel):
    organization_id: int
    item_id: int
    item_name: str
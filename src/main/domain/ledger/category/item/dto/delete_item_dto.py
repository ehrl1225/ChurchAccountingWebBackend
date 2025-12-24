from pydantic import BaseModel

class DeleteItemDto(BaseModel):
    organization_id: int
    item_id: int
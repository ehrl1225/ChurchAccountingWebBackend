from typing import Optional

from pydantic import BaseModel

class EditAllItemDto(BaseModel):
    category_id: int
    id: Optional[int]
    name: str
    deleted: bool
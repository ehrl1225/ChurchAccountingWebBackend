from pydantic import BaseModel

class ItemResponseDto(BaseModel):
    id: int
    name: str
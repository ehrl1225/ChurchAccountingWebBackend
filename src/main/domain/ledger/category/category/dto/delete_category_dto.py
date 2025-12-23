from pydantic import BaseModel

class DeleteCategoryDto(BaseModel):
    category_id: int
from pydantic import BaseModel

class EditCategoryDto(BaseModel):
    organization_id: int
    category_id: int
    category_name:str
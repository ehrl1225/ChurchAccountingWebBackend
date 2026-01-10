from pydantic import BaseModel

class ImportCategoryDto(BaseModel):
    from_organization_id: int
    from_organization_year: int
    to_organization_id: int
    to_organization_year: int
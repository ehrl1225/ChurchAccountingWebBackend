from pydantic import BaseModel

class OrganizationCreateDto(BaseModel):
    name: str
    description: str
    start_year: int
    end_year: int
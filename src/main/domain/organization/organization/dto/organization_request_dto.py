from pydantic import BaseModel

class OrganizationRequestDto(BaseModel):
    name: str
    description: str
    start_year: int
    end_year: int
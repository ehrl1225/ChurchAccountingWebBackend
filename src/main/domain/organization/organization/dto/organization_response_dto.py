from pydantic import BaseModel
from domain.organization.joined_organization.dto import JoinedOrganizationResponse

class OrganizationResponseDto(BaseModel):
    id: int
    name: str
    description: str
    start_year: int
    end_year: int
    members: list[JoinedOrganizationResponse]
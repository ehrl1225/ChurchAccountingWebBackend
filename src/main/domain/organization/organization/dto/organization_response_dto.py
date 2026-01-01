from typing import Optional

from pydantic import BaseModel, ConfigDict

from common.database import MemberRole
from domain.organization.joined_organization.dto import JoinedOrganizationResponse

class OrganizationResponseDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_year: int
    end_year: int
    my_role: Optional[MemberRole] = None
    members: list[JoinedOrganizationResponse] = []

    model_config = ConfigDict(from_attributes=True)
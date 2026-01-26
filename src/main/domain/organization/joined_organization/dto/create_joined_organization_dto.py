from pydantic import BaseModel
from common.enum.member_role import MemberRole

class CreateJoinedOrganizationDto(BaseModel):
    organization_id: int
    member_id: int
    member_role: MemberRole
from pydantic import BaseModel

from common.database import MemberRole


class JoinedOrganizationResponse(BaseModel):
    id: int
    member_name:str
    member_role: MemberRole
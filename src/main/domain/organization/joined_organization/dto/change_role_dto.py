from pydantic import BaseModel
from common.enum.member_role import MemberRole

class ChangeRoleDto(BaseModel):
    member_id: int
    member_role: MemberRole
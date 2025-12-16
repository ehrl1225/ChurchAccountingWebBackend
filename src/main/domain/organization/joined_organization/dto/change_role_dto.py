from pydantic import BaseModel
from common.database import MemberRole

class ChangeRoleDto(BaseModel):
    member_id: int
    member_role: MemberRole
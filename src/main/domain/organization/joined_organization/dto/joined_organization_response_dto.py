from typing import Optional

from pydantic import BaseModel, ConfigDict

from common.enum.member_role import MemberRole


class JoinedOrganizationResponse(BaseModel):
    id: int
    member_id: int
    member_name:Optional[str] = None
    member_role: MemberRole

    model_config = ConfigDict(from_attributes=True)
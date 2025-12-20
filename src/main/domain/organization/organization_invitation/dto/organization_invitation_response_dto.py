from pydantic import BaseModel

class OrganizationInvitationResponseDto(BaseModel):
    id: int
    invitor_name: str
    organization_id: int
    organization_name: str
from pydantic import BaseModel

class CreateOrganizationInvitationDto(BaseModel):
    organization_id: int
    email: str

from pydantic import BaseModel

class DeleteEventDto(BaseModel):
    organization_id: int
    event_id: int
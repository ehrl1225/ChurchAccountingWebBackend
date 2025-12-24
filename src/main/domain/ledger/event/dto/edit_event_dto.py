from datetime import date

from pydantic import BaseModel

class EditEventDto(BaseModel):
    event_id: int
    organization_id: int
    event_name: str
    start_date: date
    end_date: date
    description: str
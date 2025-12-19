from pydantic import BaseModel
from datetime import date

class CreateEventDTO(BaseModel):
    organization_id: int
    year: int
    name: str
    start_date: date
    end_date: date
    description: str
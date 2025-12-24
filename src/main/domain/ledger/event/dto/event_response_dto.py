from pydantic import BaseModel
from datetime import date

class EventResponseDTO(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    description: str
from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date

class EventResponseDTO(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
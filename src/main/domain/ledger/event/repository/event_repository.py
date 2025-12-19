from sqlalchemy.orm import Session

from domain.ledger.event.dto import CreateEventDTO
from domain.organization.organization.entity import Organization
from domain.ledger.event.entity import Event


class EventRepository:


    async def create_event(
            self,
            db:Session,
            organization: Organization,
            create_event_dto: CreateEventDTO
    ):
        event = Event(
            name=create_event_dto.name,
            start_date=create_event_dto.start_date,
            end_date=create_event_dto.end_date,
            organization=organization,
            year=create_event_dto.year,
        )
        db.add(event)
        db.flush()
        return event

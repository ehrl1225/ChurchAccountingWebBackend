from sqlalchemy.orm import Session
from typing import Optional

from domain.ledger.event.dto import CreateEventDTO
from domain.organization.organization.entity import Organization
from domain.ledger.event.entity import Event


class EventRepository:


    async def create_event(
            self,
            db:Session,
            create_event_dto: CreateEventDTO
    ):
        event = Event(
            name=create_event_dto.name,
            start_date=create_event_dto.start_date,
            end_date=create_event_dto.end_date,
            organization_id=create_event_dto.organization_id,
            year=create_event_dto.year,
        )
        db.add(event)
        db.flush()
        db.refresh(event)
        return event

    async def find_event_by_id(self, db:Session, id:int) -> Optional[Event]:
        return db.query(Event).get(id)

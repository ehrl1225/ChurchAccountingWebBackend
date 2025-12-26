from sqlalchemy.orm import Session
from typing import Optional

from sqlalchemy.sql.operators import and_

from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.edit_event_dto import EditEventDto
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
        return db.get(Event, id)

    async def find_all(self, db:Session, organization_id:int, year:int) -> list[Event]:
        events = (db
                  .query(Event)
                  .filter(and_(Event.organization_id == organization_id,
                               Event.year == year))
                  .all())
        return events

    async def update(self, db:Session, event:Event, edit_event_dto:EditEventDto):
        event.name = edit_event_dto.event_name
        event.start_date = edit_event_dto.start_date
        event.end_date = edit_event_dto.end_date
        event.description = edit_event_dto.description
        db.flush()
        db.refresh(event)

    async def delete(self, db:Session, event:Event):
        db.delete(event)
        db.flush()
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.sql.operators import and_

from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.organization.organization.entity import Organization
from domain.ledger.event.entity import Event


class EventRepository:


    async def create_event(
            self,
            db:AsyncSession,
            create_event_dto: CreateEventDTO
    ):
        event = Event(
            name=create_event_dto.name,
            start_date=create_event_dto.start_date,
            end_date=create_event_dto.end_date,
            organization_id=create_event_dto.organization_id,
            year=create_event_dto.year,
        )
        await db.add(event)
        await db.flush()
        await db.refresh(event)
        return event

    async def find_by_id(self, db:AsyncSession, id:int) -> Optional[Event]:
        return await db.get(Event, id)

    async def find_by_organization_and_id(self, db:AsyncSession, organization_id:int, event_id:int) -> Optional[Event]:
        query = (select(Event)
                 .filter(Event.organization_id == organization_id)
                 .filter(Event.id == event_id))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self, db:AsyncSession, organization_id:int, year:int) -> list[Event]:
        query = (select(Event)
                 .filter(Event.organization_id==organization_id)
                 .filter(Event.year==year))
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db:AsyncSession, event:Event, edit_event_dto:EditEventDto):
        event.name = edit_event_dto.event_name
        event.start_date = edit_event_dto.start_date
        event.end_date = edit_event_dto.end_date
        event.description = edit_event_dto.description
        await db.flush()
        await db.refresh(event)

    async def delete(self, db:AsyncSession, event:Event):
        await db.delete(event)
        await db.flush()
from sqlalchemy.orm import Session

from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.repository import EventRepository


class EventService:

    def __init__(
            self,
            event_repository: EventRepository,

    ):
        self.event_repository = event_repository

    async def create_event(self, db:Session, create_event_dto:CreateEventDTO):
        await self.event_repository.create_event(db, create_event_dto)
from sqlalchemy.orm import Session

from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.delete_event_dto import DeleteEventDto
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.ledger.event.dto.event_response_dto import EventResponseDTO
from domain.ledger.event.dto.search_event_params import SearchEventParams
from domain.ledger.event.repository import EventRepository


class EventService:

    def __init__(
            self,
            event_repository: EventRepository,

    ):
        self.event_repository = event_repository

    async def create_event(self, db:Session, create_event_dto:CreateEventDTO):
        await self.event_repository.create_event(db, create_event_dto)

    async def find_all(self, db:Session, search_event_params:SearchEventParams):
        events = await self.event_repository.find_all(
            db=db,
            organization_id=search_event_params.organization_id,
            year=search_event_params.year)
        return [EventResponseDTO.model_validate(event) for event in events]

    async def update(self, db:Session, edit_event_dto:EditEventDto):
        event = await self.event_repository.find_event_by_id(db, id=edit_event_dto.event_id)
        await self.event_repository.update(db, event, edit_event_dto)

    async def delete(self, db:Session, delete_event_dto:DeleteEventDto):
        event = await self.event_repository.find_event_by_id(db, id=delete_event_dto.event_id)
        await self.event_repository.delete(db, event)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.delete_event_params import DeleteEventParams
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.ledger.event.dto.event_response_dto import EventResponseDTO
from domain.ledger.event.dto.search_event_params import SearchEventParams
from domain.ledger.event.repository import EventRepository
from domain.organization.organization.repository import OrganizationRepository


class EventService:

    def __init__(
            self,
            event_repository: EventRepository,
            organization_repository: OrganizationRepository,

    ):
        self.event_repository = event_repository
        self.organization_repository = organization_repository

    async def create_event(self, db: AsyncSession, create_event_dto:CreateEventDTO):
        # verify
        if create_event_dto.end_date < create_event_dto.start_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date cannot be before start date")
        if create_event_dto.start_date.year != create_event_dto.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Start year must be equal to year")
        if create_event_dto.end_date.year != create_event_dto.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End year must be equal to year")
        organization = await self.organization_repository.find_by_id(db, create_event_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if not organization.start_year <= create_event_dto.year <= organization.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not available year")

        # work
        await self.event_repository.create_event(db, create_event_dto)

    async def find_all(self, db: AsyncSession, search_event_params:SearchEventParams):
        # verify
        organization = await self.organization_repository.find_by_id(db, search_event_params.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if not organization.start_year <= search_event_params.year <= organization.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not available year")

        # work
        events = await self.event_repository.find_all(
            db=db,
            organization_id=search_event_params.organization_id,
            year=search_event_params.year)
        return [EventResponseDTO.model_validate(event) for event in events]

    async def update(self, db: AsyncSession, edit_event_dto:EditEventDto):
        # verify
        if edit_event_dto.end_date < edit_event_dto.start_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date cannot be before start date")
        event = await self.event_repository.find_by_organization_and_id(
            db,
            organization_id=edit_event_dto.organization_id,
            event_id=edit_event_dto.event_id)
        if event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        if edit_event_dto.start_date.year != event.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Start year must be equal to year")
        if edit_event_dto.end_date.year != event.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End year must be equal to year")

        # work
        await self.event_repository.update(db, event, edit_event_dto)

    async def delete(self, db: AsyncSession, delete_event_dto:DeleteEventParams):
        # verify
        event = await self.event_repository.find_by_organization_and_id(
            db,
            organization_id=delete_event_dto.organization_id,
            event_id=delete_event_dto.event_id)
        if event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # work
        await self.event_repository.delete(db, event)
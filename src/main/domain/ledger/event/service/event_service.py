from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.repository import EventRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization


class EventService:

    def __init__(
            self,
            event_repository: EventRepository,

    ):
        self.event_repository = event_repository

    async def create_event(self, db:Session, create_event_dto:CreateEventDTO):
        await self.event_repository.create_event(db, create_event_dto)
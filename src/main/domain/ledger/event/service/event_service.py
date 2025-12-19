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
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,

    ):
        self.event_repository = event_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository

    async def create_event(self, db:Session, me_dto:MemberDTO, create_event_dto:CreateEventDTO):
        me = await self.member_repository.find_by_id(me_dto.id)
        organization = await self.organization_repository.find_by_id(db, create_event_dto.organizaiton_id)
        joined_organization: JoinedOrganization = await self.joined_organization_repository.find_by_member_and_organization(db, me, organization)
        if joined_organization.member_role not in [MemberRole.READ_WRITE, MemberRole.ADMIN, MemberRole.OWNER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Member role not allowed")
        await self.event_repository.create_event(db, organization, create_event_dto)
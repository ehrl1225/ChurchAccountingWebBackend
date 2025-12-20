from fastapi import HTTPException
from sqlalchemy.orm import Session

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.organization.joined_organization.dto.create_joined_organization_dto import CreateJoinedOrganizationDto
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization.dto import OrganizationCreateDto
from domain.member.repository import MemberRepository


class OrganizationService:

    def __init__(
            self,
            organization_repository: OrganizationRepository,
            organization_member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,
    ):
        self.organization_repository = organization_repository
        self.joined_organization_repository = joined_organization_repository
        self.organization_member_repository = organization_member_repository

    async def create(self, db:Session, member_dto:MemberDTO, organization_create_dto:OrganizationCreateDto):
        organization =  await self.organization_repository.create(db, organization_create_dto)
        member = await self.organization_member_repository.find_by_id(db, member_dto.id)
        if not member:
            raise HTTPException(status_code=400, detail="Member not found")
        await self.joined_organization_repository.join_organization(db, CreateJoinedOrganizationDto(
            organization_id=organization.id,
            member_id=member.id,
            member_role=MemberRole.OWNER,
        ))
        return organization

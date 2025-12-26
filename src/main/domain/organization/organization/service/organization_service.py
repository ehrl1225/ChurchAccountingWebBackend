from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization.dto import OrganizationRequestDto
from domain.member.entity import Member
from domain.member.repository import MemberRepository


class OrganizationService:

    def __init__(
            self,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,
    ):
        self.organization_repository = organization_repository
        self.joined_organization_repository = joined_organization_repository
        self.member_repository = member_repository

    async def create(self, db:Session, member_dto:MemberDTO, organization_request_dto:OrganizationRequestDto):
        if not organization_request_dto.start_year <= organization_request_dto.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization end year must be greater than the start year")
        organization =  await self.organization_repository.create(db, organization_request_dto)
        member: Member = await self.member_repository.find_by_id(db, member_dto.id)
        if not member:
            raise HTTPException(status_code=400, detail="Member not found")
        await self.joined_organization_repository.join_organization(db, CreateJoinedOrganizationDto(
            organization_id=organization.id,
            member_id=member.id,
            member_role=MemberRole.OWNER,
        ))
        return organization

    async def update(self, db:Session, organization_id:int, organization_request_dto:OrganizationRequestDto):
        if not organization_request_dto.start_year <= organization_request_dto.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization end year must be greater than the start year")
        organization = await self.organization_repository.find_by_id(db, organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        await self.organization_repository.update(db, organization, organization_request_dto)

    async def delete(self, db:Session, organization_id:int) -> None:
        organization = await self.organization_repository.find_by_id(db, organization_id)
        await self.organization_repository.soft_delete(db, organization)

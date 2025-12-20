from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.joined_organization.dto import ChangeRoleDto
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization

class JoinedOrganizationService:

    def __init__(
            self,
            joined_organization_repository: JoinedOrganizationRepository,
            member_repository: MemberRepository,
            organization_repository: OrganizationRepository,
    ):
        self.joined_organization_repository = joined_organization_repository
        self.member_repository = member_repository
        self.organization_repository = organization_repository

    async def change_member_role(
            self,
            db:Session,
            organization_id:int,
            change_role: ChangeRoleDto
    ):
        organization = await self.organization_repository.find_by_id(db, organization_id)
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        member = await self.member_repository.find_by_id(db, change_role.member_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        joined_organization = await self.joined_organization_repository.find_by_member_and_organization(db, member, organization)
        if not joined_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not joined organization")
        await self.joined_organization_repository.change_member_role(db, joined_organization, change_role.member_role)



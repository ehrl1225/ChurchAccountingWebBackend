from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.joined_organization.dto import ChangeRoleDto, JoinedOrganizationResponse
from domain.organization.organization.dto.organization_response_dto import OrganizationResponseDto
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization
from domain.organization.organization.entity import Organization
from domain.member.entity import Member

class JoinedOrganizationService:

    def __init__(
            self,
            joined_organization_repository: JoinedOrganizationRepository,
            member_repository: MemberRepository,
            organization_repository: OrganizationRepository,
    ):
        self.joined_organization_repository:JoinedOrganizationRepository = joined_organization_repository
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


    async def get_all_joined_organizations(
            self,
            db:Session,
            me_dto:MemberDTO
    ):
        member = await self.member_repository.find_by_id(db, me_dto.member_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        joined_organizations:list[JoinedOrganization] = self.joined_organization_repository.find_all_by_member(db, member.id)
        organizations = []
        for joined_organization in joined_organizations:
            organization:Organization = joined_organization.organization
            organization_dto = OrganizationResponseDto.model_validate(organization)
            members = []
            joined_members:list[JoinedOrganization] = organization.joined_organization
            for joined_member in joined_members:
                member:Member = joined_member.member
                joined_member_dto = JoinedOrganizationResponse.model_validate(joined_member)
                joined_member_dto.member_name = member.name
                members.append(joined_member_dto)
            organization_dto.members = members
            organizations.append(organization_dto)

        return organizations

    async def delete_joined_organization(
            self,
            db:Session,
            joined_organization_id:int,
    ):
        joined_organization = await self.joined_organization_repository.find_by_id(db, joined_organization_id)
        if not joined_organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JoinedOrganization not found")
        await self.joined_organization_repository.delete_joined_organization(db, joined_organization)
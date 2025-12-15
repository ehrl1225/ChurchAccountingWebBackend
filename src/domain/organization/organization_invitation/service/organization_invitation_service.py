from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database.member_role import MemberRole
from common.security.member_DTO import MemberDTO
from domain.member.entity import Member
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization_invitation.entity import StatusEnum, OrganizationInvitation
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto
from domain.organization.organization.repository import OrganizationRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.entity import JoinedOrganization

class OrganizationInvitationService:

    def __init__(
            self,
            organization_invitation_repository: OrganizationInvitationRepository,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository
    ):
        self.organization_invitation_repository = organization_invitation_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository

    async def create(self, db:Session,me_dto:MemberDTO, create_invitation_dto: CreateOrganizationInvitationDto):
        organization = await self.organization_repository.find_by_id(db, create_invitation_dto.organization_id)
        me = await self.member_repository.find_by_id(db, me_dto.id)
        joined_organization:JoinedOrganization = self.joined_organization_repository.find_by_member_and_organization(db, me, organization)
        if joined_organization.member_role not in [MemberRole.ADMIN, MemberRole.OWNER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        member = await self.member_repository.get_member_by_email(db, create_invitation_dto.email)
        invitation = await self.organization_invitation_repository.create_invitation(db, organization, member)
        return invitation

    async def update(self, db:Session, me_dto:MemberDTO , organization_invitation_id:int, status_enum: StatusEnum):
        organization_invitation: OrganizationInvitation = await self.organization_invitation_repository.find_by_id(db, organization_invitation_id)
        if organization_invitation.member_id != me_dto.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        if status_enum == StatusEnum.ACCEPTED:
            organization = await self.organization_repository.find_by_id(db, organization_invitation.organization_id)
            me = await self.member_repository.find_by_id(db, me_dto.id)
            self.joined_organization_repository.join_organization(db, organization, me, MemberRole.READ_ONLY)
        await self.organization_invitation_repository.update_invitation_status(db, organization_invitation, status_enum)




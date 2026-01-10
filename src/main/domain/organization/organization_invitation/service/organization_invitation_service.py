from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.member_role import MemberRole
from common.security.member_DTO import MemberDTO
from domain.member.entity import Member
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.entity import Organization
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto, \
    OrganizationInvitationResponseDto
from domain.organization.organization_invitation.entity import StatusEnum, OrganizationInvitation
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository


class OrganizationInvitationService:

    def __init__(
            self,
            organization_invitation_repository: OrganizationInvitationRepository,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,
            redis_client: Redis
    ):
        self.organization_invitation_repository = organization_invitation_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository
        self.redis_client = redis_client

    async def create(self, db: AsyncSession,me_dto:MemberDTO, create_invitation_dto: CreateOrganizationInvitationDto):
        organization = await self.organization_repository.find_by_id(db, create_invitation_dto.organization_id)
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        member = await self.member_repository.find_by_email(db, create_invitation_dto.email)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        invitation = await self.organization_invitation_repository.create_invitation(db, organization, member, me_dto.id)
        channel = f"invitations: {create_invitation_dto.member.id}"
        await self.redis_client.publish(channel, "Invitation received")
        return invitation

    async def update(self, db: AsyncSession, me_dto:MemberDTO , organization_invitation_id:int, status_enum: StatusEnum):
        organization_invitation: OrganizationInvitation = await self.organization_invitation_repository.find_by_id(db, organization_invitation_id)
        if not organization_invitation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization invitation not found")
        if organization_invitation.member_id != me_dto.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong invitation")
        if status_enum == StatusEnum.ACCEPTED:
            organization = await self.organization_repository.find_by_id(db, organization_invitation.organization_id)
            if not organization:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
            me = await self.member_repository.find_by_id(db, me_dto.id)
            await self.joined_organization_repository.join_organization(db, CreateJoinedOrganizationDto(
                organization_id=organization.id,
                member_id=me.id,
                member_role=MemberRole.READ_ONLY
            ))
        await self.organization_invitation_repository.update_invitation_status(db, organization_invitation, status_enum)
        channel = f"invitations: {me_dto.id}"
        await self.redis_client.publish(channel, "Invitation updated")

    async def get_invitations(self, db: AsyncSession, me_dto:MemberDTO) -> list[OrganizationInvitationResponseDto]:
        invitation_dto_list:list[OrganizationInvitationResponseDto] = []
        invitations = await self.organization_invitation_repository.find_pending_by_member_id(db, me_dto.id)
        for organization_invitation in invitations:
            invitor:Member = organization_invitation.invitor
            organization: Organization = organization_invitation.organization
            invitation_dto_list.append(
                OrganizationInvitationResponseDto(
                    id=organization_invitation.id,
                    invitor_name=invitor.name,
                    organization_id=organization.id,
                    organization_name=organization.name,
                )
            )
        return invitation_dto_list

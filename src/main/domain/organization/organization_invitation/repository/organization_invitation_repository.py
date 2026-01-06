from typing import Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.operators import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.organization_invitation.entity import OrganizationInvitation, StatusEnum


class OrganizationInvitationRepository:

    async def create_invitation(self, db:AsyncSession, organization:Organization, member: Member, me_id:int):
        organization_invitation = OrganizationInvitation(
            organization_id=organization.id,
            member_id=member.id,
            status=StatusEnum.PENDING,
            invitor_id=me_id
        )
        db.add(organization_invitation)
        await db.flush()
        await db.refresh(organization_invitation)
        return organization_invitation

    async def update_invitation_status(
            self,
            db:AsyncSession,
            organization_invitation:OrganizationInvitation,
            staus_enum: StatusEnum
    ):
        organization_invitation.status = staus_enum
        await db.flush()
        await db.refresh(organization_invitation)
        return organization_invitation

    async def find_by_id(self, db:AsyncSession, id:int) -> Optional[OrganizationInvitation]:
        return await db.get(OrganizationInvitation, id)

    async def find_pending_by_member_id(self, db:AsyncSession, member_id:int) -> list[OrganizationInvitation]:
        query = (select(OrganizationInvitation)
                 .options(
                    joinedload(OrganizationInvitation.invitor),
                    joinedload(OrganizationInvitation.organization))
                 .filter(OrganizationInvitation.member_id == member_id)
                 .filter(OrganizationInvitation.status == StatusEnum.PENDING))
        result = await db.execute(query)
        return result.scalars().all()
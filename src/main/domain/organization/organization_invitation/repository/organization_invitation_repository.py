from typing import Optional

from sqlalchemy.orm import Session

from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.organization_invitation.entity import OrganizationInvitation, StatusEnum


class OrganizationInvitationRepository:

    async def create_invitation(self, db:Session, organization:Organization, member: Member):
        organization_invitation = OrganizationInvitation(
            organization_id=organization.id,
            member_id=member.id,
            status=StatusEnum.PENDING
        )
        db.add(organization_invitation)
        db.flush()
        db.refresh(organization_invitation)
        return organization_invitation

    async def update_invitation_status(
            self,
            db:Session,
            organization_invitation:OrganizationInvitation,
            staus_enum: StatusEnum
    ):
        organization_invitation.status = staus_enum
        db.flush()
        db.refresh(organization_invitation)
        return organization_invitation

    async def find_by_id(self, db:Session, id:int) -> Optional[OrganizationInvitation]:
        return db.query(OrganizationInvitation).get(id)
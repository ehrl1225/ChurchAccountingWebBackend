from sqlalchemy import and_
from sqlalchemy.orm import Session

from common.database import MemberRole
from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.joined_organization.entity import JoinedOrganization

class JoinedOrganizationRepository:

    async def join_organization(
            self,
            db: Session,
            organization: Organization,
            member: Member,
            member_role:MemberRole
    ):
        joined_organization = JoinedOrganization(
            member_role=member_role,
            organization_id=organization.id,
            member_id=member.id,
            organization=organization,
            member=member,
        )
        db.add(joined_organization)
        db.flush()
        db.refresh(joined_organization)
        return joined_organization

    async def find_by_member_and_organization(self, db: Session, member: Member, organization: Organization):
        joined_organization = (db
                               .query(JoinedOrganization)
                               .filter(and_(JoinedOrganization.member_id == member.id,
                                            JoinedOrganization.organization_id == organization.id))
                               .one_or_none())
        return joined_organization

    async def change_member_role(self, db: Session, joined_organization: JoinedOrganization, member_role: MemberRole):
        joined_organization.member_role = member_role
        db.flush()
        db.refresh(joined_organization)
        return joined_organization
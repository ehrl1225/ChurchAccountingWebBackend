from sqlalchemy.orm import Session

from common.database import MemberRole
from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.joined_organization.entity import JoinedOrganization

class JoinedOrganizationRepository:

    def join_organization(
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
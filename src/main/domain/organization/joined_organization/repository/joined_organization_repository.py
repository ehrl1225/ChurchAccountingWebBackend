from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from common.database import MemberRole
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.joined_organization.entity import JoinedOrganization

class JoinedOrganizationRepository:

    async def join_organization(
            self,
            db: Session,
            create_joined_organization: CreateJoinedOrganizationDto
    ):
        joined_organization = JoinedOrganization(
            member_role=create_joined_organization.member_role,
            organization_id=create_joined_organization.organization_id,
            member_id=create_joined_organization.member_id,
            joined_at=datetime.now(),
        )
        db.add(joined_organization)
        db.flush()
        db.refresh(joined_organization)
        return joined_organization

    async def find_by_member_and_organization(self, db: Session, member: Member, organization: Organization) -> Optional[JoinedOrganization]:
        joined_organization = (db
                               .query(JoinedOrganization)
                               .filter(and_(JoinedOrganization.member_id == member.id,
                                            JoinedOrganization.organization_id == organization.id))
                               .one_or_none())
        return joined_organization

    async def find_by_id(self, db: Session, id: int) -> Optional[JoinedOrganization]:
        return db.get(JoinedOrganization, id)

    async def change_member_role(self, db: Session, joined_organization: JoinedOrganization, member_role: MemberRole):
        joined_organization.member_role = member_role
        db.flush()
        db.refresh(joined_organization)
        return joined_organization

    async def find_all_by_member(self, db: Session, member_id: int):
        joined_organizations = (db
                                .query(JoinedOrganization)
                                .filter(JoinedOrganization.member_id == member_id)
                                .all())
        return joined_organizations

    async def delete_joined_organization(self, db: Session, joined_organization: JoinedOrganization):
        db.delete(joined_organization)
        db.flush()
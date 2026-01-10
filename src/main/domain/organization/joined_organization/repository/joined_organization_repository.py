from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import MemberRole
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.organization.entity import Organization
from domain.member.entity import Member
from domain.organization.joined_organization.entity import JoinedOrganization

class JoinedOrganizationRepository:

    async def join_organization(
            self,
            db: AsyncSession,
            create_joined_organization: CreateJoinedOrganizationDto
    ):
        joined_organization = JoinedOrganization(
            member_role=create_joined_organization.member_role,
            organization_id=create_joined_organization.organization_id,
            member_id=create_joined_organization.member_id,
            joined_at=datetime.now(),
        )
        db.add(joined_organization)
        await db.flush()
        await db.refresh(joined_organization)
        return joined_organization

    async def find_by_member_and_organization(self, db: AsyncSession, member: Member, organization: Organization) -> Optional[JoinedOrganization]:
        query = (select(JoinedOrganization)
                 .filter(JoinedOrganization.member_id == member.id)
                 .filter(JoinedOrganization.organization_id == organization.id)
                 )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_id(self, db: AsyncSession, id: int) -> Optional[JoinedOrganization]:
        return await db.get(JoinedOrganization, id)

    async def change_member_role(self, db: AsyncSession, joined_organization: JoinedOrganization, member_role: MemberRole):
        joined_organization.member_role = member_role
        await db.flush()
        await db.refresh(joined_organization)
        return joined_organization

    async def find_all_by_member(self, db: AsyncSession, member_id: int):
        query = (select(JoinedOrganization)
                 .join(JoinedOrganization.organization)
                 .options(
                    joinedload(JoinedOrganization.organization)
                    .selectinload(Organization.joined_organizations)
                    .joinedload(JoinedOrganization.member))
                 .filter(JoinedOrganization.member_id == member_id)
                 .filter(Organization.deleted == False))
        result = await db.execute(query)
        return result.scalars().all()

    async def delete_joined_organization(self, db: AsyncSession, joined_organization: JoinedOrganization):
        await db.delete(joined_organization)
        await db.flush()
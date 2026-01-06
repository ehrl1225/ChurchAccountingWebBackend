from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.sql.operators import and_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.organization.organization.entity import Organization
from domain.organization.organization.dto import OrganizationRequestDto
from typing import Optional

class OrganizationRepository:

    async def create(self, db: AsyncSession, organization_request_dto: OrganizationRequestDto) -> Organization:
        organization = Organization(
            name=organization_request_dto.name,
            description=organization_request_dto.description,
            start_year=organization_request_dto.start_year,
            end_year=organization_request_dto.end_year,
        )
        db.add(organization)
        await db.flush()
        await db.refresh(organization)
        return organization

    async def find_by_id(self, db: AsyncSession, id: int) -> Optional[Organization]:
        organization = await db.get(Organization, id)
        return organization

    async def update(self, db:AsyncSession, organization:Organization, organization_request_dto:OrganizationRequestDto) -> None:
        organization.name = organization_request_dto.name
        organization.description = organization_request_dto.description
        organization.start_year = organization_request_dto.start_year
        organization.end_year = organization_request_dto.end_year
        await db.flush()
        await db.refresh(organization)

    async def hard_delete(self, db: AsyncSession, organization:Organization) -> None:
        await db.delete(organization)
        await db.flush()

    async def soft_delete(self, db: AsyncSession, organization:Organization) -> None:
        organization.deleted = True
        organization.deleted_at = datetime.now()
        await db.flush()
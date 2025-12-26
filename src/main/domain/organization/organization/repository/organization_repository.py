from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_

from domain.organization.organization.entity import Organization
from domain.organization.organization.dto import OrganizationRequestDto
from typing import Optional

class OrganizationRepository:

    async def create(self, db: Session, organization_request_dto: OrganizationRequestDto) -> Organization:
        organization = Organization(
            name=organization_request_dto.name,
            description=organization_request_dto.description,
            start_year=organization_request_dto.start_year,
            end_year=organization_request_dto.end_year,
        )
        db.add(organization)
        db.flush()
        db.refresh(organization)
        return organization

    async def find_by_id(self, db: Session, id: int) -> Optional[Organization]:
        organization = db.get(Organization, id)
        return organization

    async def update(self, db:Session, organization:Organization, organization_request_dto:OrganizationRequestDto) -> None:
        organization.name = organization_request_dto.name
        organization.description = organization_request_dto.description
        organization.start_year = organization_request_dto.start_year
        organization.end_year = organization_request_dto.end_year
        db.flush()
        db.refresh(organization)

    async def hard_delete(self, db: Session, organization:Organization) -> None:
        db.delete(organization)
        db.flush()

    async def soft_delete(self, db: Session, organization:Organization) -> None:
        organization.deleted = True
        organization.deleted_at = datetime.now()
        db.flush()
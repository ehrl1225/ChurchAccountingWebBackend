from datetime import datetime

from sqlalchemy.orm import Session
from domain.organization.organization.entity import Organization
from domain.organization.organization.dto import OrganizationCreateDto
from typing import Optional

class OrganizationRepository:

    async def create(self, db: Session, organization_create_dto: OrganizationCreateDto):
        organization = Organization(
            name=organization_create_dto.name,
            description=organization_create_dto.description,
            start_year=organization_create_dto.start_year,
            end_year=organization_create_dto.end_year,
        )
        db.add(organization)
        db.flush()
        db.refresh(organization)
        return organization

    async def find_by_id(self, db: Session, id: int) -> Optional[Organization]:
        organization = db.query(Organization).get(id)
        return organization

    async def hard_delete(self, db: Session, organization:Organization) -> None:
        db.delete(organization)
        db.flush()

    async def soft_delete(self, db: Session, organization:Organization) -> None:
        organization.deleted = True
        organization.deleted_at = datetime.now()
        db.flush()
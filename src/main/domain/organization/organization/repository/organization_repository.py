from sqlalchemy.orm import Session
from domain.organization.organization.entity import Organization
from domain.organization.organization.dto import OrganizationCreateDto

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

    async def find_by_id(self, db: Session, id: int) -> Organization:
        organization = db.query(Organization).get(id)
        return organization
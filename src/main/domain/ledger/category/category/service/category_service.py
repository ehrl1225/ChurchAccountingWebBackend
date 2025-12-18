from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization
from domain.organization.organization.repository import OrganizationRepository
from common.security.member_DTO import MemberDTO


class CategoryService:

    def __init__(
            self,
            category_repository: CategoryRepository,
            item_repository: ItemRepository,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,
    ):
        self.category_repository = category_repository
        self.item_repository = item_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository

    async def create(self,db:Session, me_dto:MemberDTO, create_category: CreateCategoryDTO):
        organization = await self.organization_repository.find_by_id(db,create_category.organization_id)
        me = await self.member_repository.find_by_id(db,me_dto.id)
        joined_organization:JoinedOrganization = await self.joined_organization_repository.find_by_member_and_organization(db, me, organization)
        if joined_organization.member_role not in [MemberRole.READ_WRITE,MemberRole.ADMIN, MemberRole.OWNER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Member role not allowed")
        category = await self.category_repository.create_category(
            db=db,
            name=create_category.category_name,
            tx_type=create_category.tx_type,
            organization=organization,
            year=create_category.year,
        )
        if create_category.item_name is None or create_category.item_name == "":
            return category
        await self.item_repository.create_item(
            db=db,
            name=create_category.item_name,
            organization=organization,
            category=category,
            year=create_category.year,
        )
        return category

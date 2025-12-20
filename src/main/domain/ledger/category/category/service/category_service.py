from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from domain.ledger.category.category.entity import Category
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto
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
    ):
        self.category_repository = category_repository
        self.item_repository = item_repository

    async def create(self,db:Session, create_category: CreateCategoryDTO):
        category:Category = await self.category_repository.create_category(
            db=db,
            create_category_dto=create_category
        )
        if create_category.item_name is None or create_category.item_name == "":
            return category
        await self.item_repository.create_item(
            db=db,
            create_item_dto=CreateItemDto(
                category_id=category.id,
                item_name=create_category.item_name,
                organization_id=create_category.organization_id,
                year=create_category.year,
            )
        )
        return category

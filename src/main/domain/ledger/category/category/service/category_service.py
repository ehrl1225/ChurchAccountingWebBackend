from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.ledger.category.category.dto import CreateCategoryDTO, DeleteCategoryParams
from domain.ledger.category.category.dto.category_response_dto import CategoryResponseDto
from domain.ledger.category.category.dto.edit_category_dto import EditCategoryDto
from domain.ledger.category.category.dto.search_category_params import SearchCategoryParams
from domain.ledger.category.category.entity import Category
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.dto.item_response_dto import ItemResponseDto
from domain.ledger.category.item.entity import Item
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.receipt.entity import Receipt
from domain.organization.organization.repository import OrganizationRepository


class CategoryService:

    def __init__(
            self,
            category_repository: CategoryRepository,
            item_repository: ItemRepository,
            organization_repository: OrganizationRepository,
    ):
        self.category_repository = category_repository
        self.item_repository = item_repository
        self.organization_repository = organization_repository

    async def create(self,db:Session, create_category: CreateCategoryDTO):
        organization = await self.organization_repository.find_by_id(db, create_category.organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        if not organization.start_year <= create_category.year <= organization.end_year:
            raise HTTPException(status_code=400, detail="Invalid year")
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

    async def find_all(self, db:Session, search_category_dto:SearchCategoryParams):
        categories = await self.category_repository.find_all(db=db, search_category_dto=search_category_dto)
        category_dtos = []
        for category in categories:
            category_dto = CategoryResponseDto.model_validate(category)
            items:list[Item] = category.items
            item_dtos = []
            for item in items:
                item_dto = ItemResponseDto.model_validate(item)
                item_dtos.append(item_dto)
            category_dto.items = item_dtos
            category_dtos.append(category_dto)
        return category_dtos

    async def update(self, db:Session, edit_category_dto:EditCategoryDto):
        category = await self.category_repository.find_by_organization_and_id(db, edit_category_dto.organization_id, edit_category_dto.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.category_repository.update_category(db, category, edit_category_dto.category_name)

    async def delete(self, db:Session, delete_category:DeleteCategoryParams):
        category:Category = await self.category_repository.find_by_organization_and_id(db, delete_category.organization_id, delete_category.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        receipts:list[Receipt] = category.receipts
        if len(receipts) != 0:
            raise HTTPException(status_code=400, detail="Category has receipts")
        await self.category_repository.delete(db, category)

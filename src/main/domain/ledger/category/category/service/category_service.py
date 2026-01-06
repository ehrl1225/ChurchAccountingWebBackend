from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ledger.category.category.dto import CreateCategoryDTO, DeleteCategoryParams, CategoryResponseDto, \
    EditCategoryDto, ImportCategoryDto, SearchCategoryParams, EditAllDto
from domain.ledger.category.category.entity import Category
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto, ItemResponseDto
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

    async def create(self,db: AsyncSession, create_category: CreateCategoryDTO):
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

    async def find_all(self, db: AsyncSession, search_category_dto:SearchCategoryParams):
        categories = await self.category_repository.find_all_by_tx_type(db=db, search_category_dto=search_category_dto)
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

    async def update(self, db: AsyncSession, edit_category_dto:EditCategoryDto):
        category = await self.category_repository.find_by_organization_and_id(db, edit_category_dto.organization_id, edit_category_dto.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.category_repository.update_category(db, category, edit_category_dto.category_name)

    async def delete(self, db: AsyncSession, delete_category:DeleteCategoryParams):
        category:Category = await self.category_repository.find_by_organization_id_with_receipts(db, delete_category.organization_id, delete_category.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        receipts:list[Receipt] = category.receipts
        if len(receipts) != 0:
            raise HTTPException(status_code=400, detail="Category has receipts")
        await self.category_repository.delete(db, category)

    async def import_categories(self, db: AsyncSession, import_categories_dto:ImportCategoryDto):
        from_categories = await self.category_repository.find_all(db, import_categories_dto.from_organization_id, import_categories_dto.from_organization_year)
        to_categories = await self.category_repository.find_all(db, import_categories_dto.to_organization_id, import_categories_dto.to_organization_year)
        for from_category in from_categories:
            for to_category in to_categories:
                if from_category.name == to_category.name:
                    for from_item in from_category.items:
                        for to_item in to_category.items:
                            if from_item.item_name == to_item.item_name:
                                break
                        else:
                            await self.item_repository.create_item(db, create_item_dto=CreateItemDto(
                                organization_id=import_categories_dto.to_organization_id,
                                year=import_categories_dto.to_organization_year,
                                category_id=to_category.id,
                                item_name=from_item.item_name,
                            ))
                    break
            else:
                category = await self.category_repository.create_category(db, create_category_dto=CreateCategoryDTO(
                    organization_id=import_categories_dto.to_organization_id,
                    year=import_categories_dto.to_organization_year,
                    category_name=from_category.name,
                    item_name=None,
                    tx_type=from_category.tx_type,
                ))
                for from_item in from_category.items:
                    await self.item_repository.create_item(db, create_item_dto=CreateItemDto(
                        organization_id=import_categories_dto.to_organization_id,
                        year=import_categories_dto.to_organization_year,
                        category_id=category.id,
                        item_name=from_item.name,
                    ))

    async def edit_all(self, db: AsyncSession, edit_all_dto:EditAllDto):
        for category_dto in edit_all_dto.categories:
            if category_dto.id is None:
                category = await self.category_repository.create_category(db, create_category_dto=CreateCategoryDTO(
                    organization_id=edit_all_dto.organization_id,
                    year=edit_all_dto.year,
                    item_name=None,
                    category_name=category_dto.category_name,
                    tx_type=category_dto.tx_type,
                ))
            else:
                category = await self.category_repository.find_by_id(db, category_dto.id)
                if category_dto.deleted:
                    await self.category_repository.delete(db, category)
                    continue
                if category.name != category_dto.category_name:
                    await self.category_repository.update_category(db, category, category_dto.category_name)
            for item_dto in category_dto.items:
                if item_dto.id is None:
                    await self.item_repository.create_item(db, create_item_dto=CreateItemDto(
                        organization_id=edit_all_dto.organization_id,
                        year=edit_all_dto.year,
                        category_id=category.id,
                        item_name=item_dto.name,
                    ))
                item = await self.item_repository.find_by_id(db, item_dto.id)
                if item_dto.deleted:
                    await self.item_repository.delete_item(db, item)
                    continue
                if item.name != item_dto.category_name:
                    await self.item_repository.update_item(db, item, item_dto.name)



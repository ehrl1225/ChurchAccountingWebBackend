from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.dto.category_response_dto import CategoryResponseDto
from domain.ledger.category.category.dto.search_category_dto import SearchCategoryDto
from domain.ledger.category.category.entity import Category
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.dto.item_response_dto import ItemResponseDto
from domain.ledger.category.item.entity import Item
from domain.ledger.category.item.repository import ItemRepository


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

    async def find_all(self, db:Session, search_category_dto:SearchCategoryDto):
        categories = await self.category_repository.find_all(db=db, search_category_dto=search_category_dto)
        category_dtos = []
        for category in categories:
            category_dto = CategoryResponseDto.model_validate(category)
            items:list[Item] = category.items
            item_dtos = []
            for item in items:
                item_dto = ItemResponseDto.model_validate(item)
                item_dtos.append(ItemResponseDto.model_validate(item_dto))
            category_dto.items = item_dtos
            category_dtos.append(category_dto)
        return category_dtos

    async def update(self, db:Session, category_id:int, name:str):
        category = await self.category_repository.find_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.category_repository.update_category(db, category, name)

    async def delete(self, db:Session, category_id:int):
        category = await self.category_repository.find_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.category_repository.delete(db, category)

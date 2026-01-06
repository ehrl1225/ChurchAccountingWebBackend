from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.dto.search_category_params import SearchCategoryParams
from domain.ledger.category.category.entity import Category
from domain.organization.organization.entity import Organization
from typing import Optional


class CategoryRepository:

    async def create_category(self, db:AsyncSession, create_category_dto:CreateCategoryDTO):
        category = Category(
            name=create_category_dto.category_name,
            tx_type=create_category_dto.tx_type,
            organization_id=create_category_dto.organization_id,
            year=create_category_dto.year,
        )
        db.add(category)
        await db.flush()
        await db.refresh(category)
        return category

    async def find_by_id(self, db:AsyncSession, id:int) -> Optional[Category]:
        return await db.get(Category, id)

    async def find_by_organization_and_id(self, db:AsyncSession, organization_id:int, id:int) -> Optional[Category]:
        query = (select(Category)
                 .filter(Category.id == id)
                 .filter(Category.organization_id==organization_id))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_organization_id_with_receipts(self, db:AsyncSession, organization_id:int, id:int) -> Optional[Category]:
        query = (select(Category)
                 .options(selectinload(Category.receipts),)
                 .filter(Category.id==id)
                 .filter(Category.organization_id==organization_id)
                 )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self, db:AsyncSession, organization_id:int, year:int) -> list[Category]:
        query = (select(Category)
                 .filter(Category.organization_id==organization_id)
                 .filter(Category.year==year))
        result = await db.execute(query)
        return result.scalars().all()

    async def find_all_by_tx_type(self, db: AsyncSession, search_category_dto:SearchCategoryParams) -> list[Category]:
        query = (select(Category)
                 .options(selectinload(Category.items))
                 .filter(Category.organization_id==search_category_dto.organization_id)
                 .filter(Category.year==search_category_dto.year)
                 .filter(Category.tx_type==search_category_dto.tx_type))
        result = await db.execute(query)
        return result.scalars().all()

    async def update_category(self, db: AsyncSession, category:Category, name:str):
        category.name = name
        await db.flush()
        await db.refresh(category)

    async def delete(self, db: AsyncSession, category: Category) -> None:
        await db.delete(category)
        await db.flush()

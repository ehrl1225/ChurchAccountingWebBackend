from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.dto.request.item_check import ItemCheck
from domain.ledger.category.item.entity import Item


class ItemRepository:

    async def create_item(self, db:AsyncSession, create_item_dto:CreateItemDto):
        item = Item(
            name=create_item_dto.item_name,
            organization_id=create_item_dto.organization_id,
            category_id=create_item_dto.category_id,
            year=create_item_dto.year
        )
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return item

    async def bulk_create(self, db:AsyncSession, items:list[Item]):
        db.add_all(items)
        await db.flush()
        for item in items:
            await db.refresh(item)
        return items

    async def find_by_id(self, db:AsyncSession, id:int) -> Optional[Item]:
        return await db.get(Item, id)

    async def find_by_organization_category_and_id(self, db:AsyncSession, organization_id:int, category_id:int, item_id:int) -> Optional[Item]:
        query = (select(Item)
                 .filter(Item.organization_id == organization_id)
                 .filter(Item.category_id==category_id)
                 .filter(Item.id==item_id))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_year_and_id_with_receipts(self, db:AsyncSession, organization_id:int, category_id, item_id) -> Optional[Item]:
        query = (select(Item)
                 .options(selectinload(Item.receipts))
                 .filter(Item.organization_id == organization_id)
                 .filter(Item.category_id==category_id)
                 .filter(Item.id==item_id)
                 )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def find_all_by_names(self, db:AsyncSession, item_checks:list[ItemCheck], organization_id:int, year:int) -> list[Item]:
        if not item_checks:
            return []
        clauses = [
            and_(
                Category.name==item_check.category_name,
                Category.tx_type == item_check.tx_type,
                Item.name == item_check.item_name)
            for item_check in item_checks
        ]
        query = (
            select(Item)
            .join(Item.category)
            .options(joinedload(Item.category))
            .filter(Item.organization_id == organization_id)
            .filter(Item.year == year)
            .filter(or_(*clauses))
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def update_item(self, db:AsyncSession, item:Item, name:str):
        item.name = name
        await db.flush()
        await db.refresh(item)

    async def delete_item(self, db:AsyncSession, item:Item):
        await db.delete(item)
        await db.flush()
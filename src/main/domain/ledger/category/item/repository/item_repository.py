from typing import Optional

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ledger.category.item.dto import CreateItemDto
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

    async def update_item(self, db:AsyncSession, item:Item, name:str):
        item.name = name
        await db.flush()
        await db.refresh(item)

    async def delete_item(self, db:AsyncSession, item:Item):
        await db.delete(item)
        await db.flush()
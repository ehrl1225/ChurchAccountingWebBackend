from typing import Optional

from sqlalchemy.orm import Session

from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.entity import Item


class ItemRepository:

    async def create_item(self, db:Session, create_item_dto:CreateItemDto):
        item = Item(
            name=create_item_dto.item_name,
            organization_id=create_item_dto.organization_id,
            category_id=create_item_dto.category_id,
            year=create_item_dto.year
        )
        db.add(item)
        db.flush()
        db.refresh(item)
        return item

    async def find_item_by_id(self, db:Session, id:int) -> Optional[Item]:
        return db.get(Item, id)

    async def find_by_organization_category_and_id(self, db:Session, organization_id:int, category_id:int, item_id:int) -> Optional[Item]:
        return (db
                .query(Item)
                .filter(Item.organization_id==organization_id)
                .filter(Item.category_id==category_id)
                .filter(Item.id==item_id)
                .one_or_none())

    async def update_item(self, db:Session, item:Item, name:str):
        item.name = name
        db.flush()
        db.refresh(item)

    async def delete_item(self, db:Session, item:Item):
        db.delete(item)
        db.flush()
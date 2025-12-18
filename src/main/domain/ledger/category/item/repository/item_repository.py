from sqlalchemy.orm import Session

from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.entity import Item
from domain.organization.organization.entity import Organization


class ItemRepository:

    async def create_item(self, db:Session, name:str, organization:Organization, category:Category, year:int) -> Item:
        item = Item(
            name=name,
            organization=organization,
            category=category,
            year=year
        )
        db.add(item)
        db.flush()
        db.refresh(item)
        return item
from sqlalchemy.orm import Session

from common.database import TxType
from domain.ledger.category.category.entity import Category
from domain.organization.organization.entity import Organization
from typing import Optional


class CategoryRepository:

    async def create_category(self, db:Session, name:str, tx_type:TxType, organization:Organization, year:int) -> Category:
        category = Category(
            name=name,
            tx_type=tx_type,
            organization=organization,
            year=year
        )
        db.add(category)
        db.flush()
        db.refresh(category)
        return category

    async def find_category_by_id(self, db:Session, id:int) -> Optional[Category]:
        return db.query(Category).get(id)
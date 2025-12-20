from sqlalchemy.orm import Session

from common.database import TxType
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.entity import Category
from domain.organization.organization.entity import Organization
from typing import Optional


class CategoryRepository:

    async def create_category(self, db:Session, create_category_dto:CreateCategoryDTO) -> Category:
        category = Category(
            name=create_category_dto.category_name,
            tx_type=create_category_dto.tx_type,
            organization_id=create_category_dto.organization_id,
            year=create_category_dto.year,
        )
        db.add(category)
        db.flush()
        db.refresh(category)
        return category

    async def find_category_by_id(self, db:Session, id:int) -> Optional[Category]:
        return db.query(Category).get(id)
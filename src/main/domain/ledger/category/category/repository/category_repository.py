from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_

from common.database import TxType
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.dto.search_category_params import SearchCategoryParams
from domain.ledger.category.category.entity import Category
from domain.organization.organization.entity import Organization
from typing import Optional


class CategoryRepository:

    async def create_category(self, db:Session, create_category_dto:CreateCategoryDTO):
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

    async def find_by_id(self, db:Session, id:int) -> Optional[Category]:
        return db.get(Category, id)

    async def find_by_organization_and_id(self, db:Session, organization_id:int, id:int) -> Optional[Category]:
        return (db
                .query(Category)
                .filter(Category.id==id)
                .filter(Category.organization_id==organization_id)
                .one_or_none())

    async def find_all(self, db: Session, search_category_dto:SearchCategoryParams) -> list[Category]:
        categories = (db
                      .query(Category)
                      .filter(Category.organization_id==search_category_dto.organization_id,)
                      .filter(Category.year==search_category_dto.year)
                      .filter(Category.tx_type==search_category_dto.tx_type)
                      .all())
        return categories

    async def update_category(self, db: Session, category:Category, name:str):
        category.name = name
        db.flush()
        db.refresh(category)

    async def delete(self, db: Session, category: Category) -> None:
        db.delete(category)
        db.flush()

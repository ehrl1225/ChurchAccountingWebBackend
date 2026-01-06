from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto, DeleteItemParams
from domain.ledger.category.item.dto.edit_item_dto import EditItemDto
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.receipt.entity import Receipt
from domain.organization.organization.repository import OrganizationRepository


class ItemService:

    def __init__(
            self,
            category_repository: CategoryRepository,
            item_repository:ItemRepository,
            organization_repository:OrganizationRepository,
    ):
        self.category_repository = category_repository
        self.item_repository:ItemRepository = item_repository
        self.organization_repository = organization_repository

    async def create_item(self, db: AsyncSession, create_item_dto:CreateItemDto):
        organization = await self.organization_repository.find_by_id(db, create_item_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if not organization.start_year <= create_item_dto.year <= organization.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong year")
        category = await self.category_repository.find_by_id(db, create_item_dto.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if organization.id != category.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Category is owned by another organization")
        await self.item_repository.create_item(
            db,
            create_item_dto
        )

    async def update_item(self, db: AsyncSession, edit_item:EditItemDto):
        item = await self.item_repository.find_by_organization_category_and_id(
            db,
            edit_item.organization_id,
            edit_item.category_id,
            edit_item.item_id
        )
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        await self.item_repository.update_item(db, item, edit_item.item_name)


    async def delete_item(self, db: AsyncSession, delete_item:DeleteItemParams):
        item = await self.item_repository.find_by_year_and_id_with_receipts(
            db,
            delete_item.organization_id,
            delete_item.category_id,
            delete_item.item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        receipts:list[Receipt] = item.receipts
        if len(receipts) != 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="only empty receipts are allowed")

        await self.item_repository.delete_item(db, item)
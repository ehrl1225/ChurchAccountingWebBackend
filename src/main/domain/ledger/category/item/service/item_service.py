from sqlalchemy.orm import Session

from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.dto.edit_item_dto import EditItemDto
from domain.ledger.category.item.repository import ItemRepository


class ItemService:

    def __init__(
            self,
            item_repository:ItemRepository,
    ):
        self.item_repository = item_repository

    async def create_item(self, db:Session, create_item_dto:CreateItemDto):
        await self.item_repository.create_item(
            db,
            create_item_dto
        )

    async def update_item(self, db:Session, edit_item:EditItemDto):
        item = await self.item_repository.find_item_by_id(db, edit_item.item_id)
        await self.item_repository.update_item(db, item, edit_item.item_name)


    async def delete_item(self, db:Session, item_id:int):
        item = await self.item_repository.find_item_by_id(db, item_id)
        await self.item_repository.delete_item(db, item)
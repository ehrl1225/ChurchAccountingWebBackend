from sqlalchemy.orm import Session

from domain.ledger.category.item.dto import CreateItemDto
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

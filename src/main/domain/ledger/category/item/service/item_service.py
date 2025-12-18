from sqlalchemy.orm import Session


class ItemService:

    def __init__(self, item_repository):
        self.item_repository = item_repository

    async def create_item(self, db:Session):
        pass
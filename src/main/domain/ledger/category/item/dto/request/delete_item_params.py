from fastapi import Query

class DeleteItemParams:
    organization_id: int
    category_id: int
    item_id: int

    def __init__(
            self,
            organization_id: int| None = Query(description="Organization ID"),
            category_id: int| None = Query(description="Category ID"),
            item_id: int| None = Query(description="Item ID"),
    ):
        self.organization_id = organization_id
        self.category_id = category_id
        self.item_id = item_id
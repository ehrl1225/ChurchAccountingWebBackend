from fastapi import Query

class DeleteCategoryParams:
    organization_id: int
    category_id: int

    def __init__(
            self,
            organization_id: int = Query(description="Organization ID"),
            category_id: int = Query(description="Category ID"),
    ):
        self.organization_id = organization_id
        self.category_id = category_id
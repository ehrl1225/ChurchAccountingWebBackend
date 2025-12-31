from fastapi import Query

class SearchAllReceiptParams:
    organization_id: int
    year: int

    def __init__(
            self,
            organization_id: int = Query(description='Organization ID'),
            year: int = Query( description='Year'),
    ):
        self.organization_id = organization_id
        self.year = year
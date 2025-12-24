from fastapi import Query

class SearchEventParams:
    organization_id: int
    year: int

    def __init__(
            self,
            organization_id:int|None = Query( description='Organization ID'),
            year:int|None = Query( description='Year'),
    ):
        self.organization_id = organization_id
        self.year = year
from fastapi import Query

class DeleteEventParams:
    organization_id: int
    event_id: int

    def __init__(
            self,
            organization_id: int = Query(description="Organization ID"),
            event_id: int = Query(description="Event ID"),
    ):
        self.organization_id = organization_id
        self.event_id = event_id
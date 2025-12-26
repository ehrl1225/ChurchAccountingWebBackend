from fastapi import Query

class DeleteJoinedOrganizationParams:
    organization_id: int
    joined_organization_id: int

    def __init__(
            self,
            organization_id: int = Query(description="Organization ID"),
            joined_organization_id: int = Query(description="Joined Organization ID")
    ):
        self.organization_id = organization_id
        self.joined_organization_id = joined_organization_id
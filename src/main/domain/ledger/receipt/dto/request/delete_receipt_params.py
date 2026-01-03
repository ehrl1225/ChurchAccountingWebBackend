from fastapi import Query

class DeleteReceiptParams:
    organization_id: int
    receipt_id: int

    def __init__(
            self,
            organization_id: int = Query(description="Organization ID"),
            receipt_id: int = Query(description="Receipt ID"),
    ):
        self.organization_id = organization_id
        self.receipt_id = receipt_id
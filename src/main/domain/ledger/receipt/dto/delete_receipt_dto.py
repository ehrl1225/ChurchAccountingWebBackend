from pydantic import BaseModel

class DeleteReceiptDto(BaseModel):
    organization_id: int
    receipt_id: int
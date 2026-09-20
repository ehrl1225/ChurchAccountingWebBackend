from pydantic import BaseModel


class MoveItemReceiptDto(BaseModel):
    organization_id: int
    from_item_id: int
    to_item_id: int
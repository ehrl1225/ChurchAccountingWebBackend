from typing import Optional

from sqlalchemy.orm import Session

from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.entity import Item
from domain.ledger.event.entity import Event
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.organization.organization.entity import Organization
from domain.ledger.receipt.entity import Receipt


class ReceiptRepository:

    async def create_receipt(
            self,
            db:Session,
            create_receipt_dto: CreateReceiptDto
    ):
        receipt = Receipt(
            receipt_image_url=create_receipt_dto.receipt_image_url,
            paper_date=create_receipt_dto.paper_date,
            actual_date=create_receipt_dto.actual_date,
            name=create_receipt_dto.name,
            tx_type=create_receipt_dto.tx_type,
            amount=create_receipt_dto.amount,
            category_id=create_receipt_dto.category_id,
            item_id=create_receipt_dto.item_id,
            event_id=create_receipt_dto.event_id,
            etc=create_receipt_dto.etc,
            organization_id=create_receipt_dto.organization_id,
            year=create_receipt_dto.year,
        )
        db.add(receipt)
        db.flush()
        db.refresh(receipt)
        return receipt
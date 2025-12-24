from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_

from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.entity import Item
from domain.ledger.event.entity import Event
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.edit_receipt_dto import EditReceiptDto
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

    async def find_by_id(self, db:Session, receipt_id:int):
        receipt = db.query(Receipt).get(receipt_id)
        return receipt

    async def find_all(self, db:Session, organization_id: int, year:int) -> list[Receipt]:
        receipts = db.query(Receipt).filter(and_(Receipt.organization_id==organization_id, Receipt.year==year)).all()
        return receipts

    async def update(self, db:Session, receipt:Receipt, edit_receipt_dto:EditReceiptDto):
        receipt.receipt_image_url = edit_receipt_dto.receipt_image_url
        receipt.paper_date = edit_receipt_dto.paper_date
        receipt.actual_date = edit_receipt_dto.actual_date
        receipt.name = edit_receipt_dto.name
        receipt.tx_type = edit_receipt_dto.tx_type
        receipt.amount = edit_receipt_dto.amount
        receipt.category_id = edit_receipt_dto.category_id
        receipt.item_id = edit_receipt_dto.item_id
        receipt.event_id = edit_receipt_dto.event_id
        receipt.etc = edit_receipt_dto.etc
        db.flush()
        db.refresh(receipt)

    async def delete(self, db:Session, receipt:Receipt):
        db.delete(receipt)
        db.flush()
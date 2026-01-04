from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_
from sqlalchemy import extract, func

from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.entity import Item
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.request.edit_receipt_dto import EditReceiptDto
from domain.ledger.receipt.dto.response import SummaryData
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
        receipt = db.get(Receipt, receipt_id)
        return receipt

    async def find_all(self, db:Session, organization_id: int, year:int) -> list[Receipt]:
        receipts = db.query(Receipt).filter(and_(Receipt.organization_id==organization_id, Receipt.year==year)).all()
        return receipts

    async def find_amount_by_month(self, db:Session, organization_id: int, year:int, month:int) -> list[SummaryData]:
        data = (db
                    .query(Category, Item, func.sum(Receipt.amount).label("total_amount"))
                    .join(Item, Receipt.item_id == Item.id)
                    .join(Category, Receipt.category_id == Category.id)
                    .filter(Receipt.organization_id==organization_id)
                    .filter(Receipt.year==year)
                    .filter(extract("month", Receipt.paper_date)==month)
                    .all())
        if data == [(None, None, None)]:
            return []
        return [SummaryData(category=category, item=item, total_amount=total_amount) for category, item, total_amount in data]

    async def find_all_amount(self, db:Session, organization_id: int, year:int) -> list[SummaryData]:
        data = (db
                .query(Category, Item, func.sum(Receipt.amount).label("total_amount"))
                .join(Item, Receipt.item_id == Item.id)
                .join(Category, Receipt.category_id==Category.id)
                .filter(Receipt.organization_id==organization_id)
                .filter(Receipt.year==year)
                .all())
        if data == [(None, None, None)]:
            return []
        return [SummaryData(category, item, total_amount) for category, item, total_amount in data]

    async def find_by_event(self, db:Session, organization_id: int, year:int, event_id:int):
        data = (db
                    .query(Category, Item, func.sum(Receipt.amount).label("total_amount"))
                    .join(Item, Receipt.item_id == Item.id)
                    .join(Category, Receipt.category_id == Category.id)
                    .filter(Receipt.organization_id==organization_id)
                    .filter(Receipt.year==year)
                    .filter(Receipt.event_id==event_id)
                    .all())
        if data == [(None, None, None)]:
            return []
        return [SummaryData(category=category, item=item, total_amount=total_amount) for category, item, total_amount in data]

    async def find_all_by_event(self, db:Session, organization_id: int, year:int):
        data = (db
                .query(Category, Item, func.sum(Receipt.amount).label("total_amount"))
                .join(Item, Receipt.item_id == Item.id)
                .join(Category, Receipt.category_id==Category.id)
                .filter(Receipt.organization_id==organization_id)
                .filter(Receipt.year==year)
                .filter(Receipt.event_id!=None)
                .all())
        if data == [(None, None, None)]:
            return []
        return [SummaryData(category=category, item=item, total_amount=total_amount) for category, item, total_amount in data]

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
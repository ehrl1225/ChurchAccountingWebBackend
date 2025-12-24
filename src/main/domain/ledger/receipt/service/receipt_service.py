from sqlalchemy.orm import Session

from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.delete_receipt_dto import DeleteReceiptDto
from domain.ledger.receipt.dto.edit_receipt_dto import EditReceiptDto
from domain.ledger.receipt.dto.receipt_response_dto import ReceiptResponseDto
from domain.ledger.receipt.dto.search_receipt_params import SearchAllReceiptParams
from domain.ledger.receipt.repository import ReceiptRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository


class ReceiptService:

    def __init__(
            self,
            receipt_repository: ReceiptRepository,
            category_repository: CategoryRepository,
            item_repository: ItemRepository,
            event_repository: EventRepository,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository
    ):
        self.receipt_repository = receipt_repository
        self.category_repository = category_repository
        self.item_repository = item_repository
        self.event_repository = event_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository

    async def create_receipt(self, db:Session, create_receipt_dto:CreateReceiptDto):
        await self.receipt_repository.create_receipt(
            db,
            create_receipt_dto
        )

    async def get_all_receipts(self, db:Session, search_receipt_params:SearchAllReceiptParams):
        receipts = await self.receipt_repository.find_all(
            db=db,
            organization_id=search_receipt_params.organization_id,
            year=search_receipt_params.year,)
        return [ReceiptResponseDto.model_validate(receipt) for receipt in receipts]

    async def update(self, db:Session, edit_receipt_dto: EditReceiptDto):
        receipt = await self.receipt_repository.find_by_id(edit_receipt_dto.receipt_id)
        await self.receipt_repository.update(db, receipt, edit_receipt_dto)

    async def delete(self, db:Session, delete_receipt_dto:DeleteReceiptDto):
        receipt = await self.receipt_repository.find_by_id(db, delete_receipt_dto.receipt_id)
        await self.receipt_repository.delete(db, receipt)
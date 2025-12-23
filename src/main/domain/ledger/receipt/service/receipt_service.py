from sqlalchemy.orm import Session

from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.dto import CreateReceiptDto
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
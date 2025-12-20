from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.repository import ReceiptRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization
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

    async def create_receipt(self, db:Session, me_dto:MemberDTO,create_receipt_dto:CreateReceiptDto):
        category = await self.category_repository.find_category_by_id(db, create_receipt_dto.category_id)
        item = await self.item_repository.find_item_by_id(db, create_receipt_dto.item_id)
        event = await self.event_repository.find_event_by_id(db, create_receipt_dto.event_id) if create_receipt_dto.event_id else None
        organization = await self.organization_repository.find_by_id(db, create_receipt_dto.organization_id)
        me = await self.member_repository.find_by_id(db, me_dto.id)
        joined_organization: JoinedOrganization = await self.joined_organization_repository.find_by_member_and_organization(db, me, organization)
        if joined_organization.member_role not in [MemberRole.READ_WRITE, MemberRole.ADMIN, MemberRole.OWNER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Member role not allowed")
        await self.receipt_repository.create_receipt(
            db,
            create_receipt_dto,
            category,
            item,
            organization,
            event
        )
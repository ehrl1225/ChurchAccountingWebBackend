from typing import Optional
from unicodedata import category

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from common.database import MemberRole
from common.security.member_DTO import MemberDTO
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.entity import Organization
from domain.ledger.category.category.repository import CategoryRepository
from domain.organization.joined_organization.entity import JoinedOrganization
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.repository import ItemRepository
from domain.member.repository import MemberRepository
from domain.organization.organization.repository import OrganizationRepository


class ItemService:

    def __init__(
            self,
            item_repository:ItemRepository,
    ):
        self.item_repository = item_repository

    async def create_item(self, db:Session, create_item_dto:CreateItemDto):
        await self.item_repository.create_item(
            db,
            create_item_dto
        )

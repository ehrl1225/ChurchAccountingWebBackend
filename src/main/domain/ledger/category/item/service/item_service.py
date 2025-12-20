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
            category_repository:CategoryRepository,
            item_repository:ItemRepository,
            member_repository:MemberRepository,
            organization_repository:OrganizationRepository,
            joined_organization_repository:JoinedOrganizationRepository,
    ):
        self.category_repository = category_repository
        self.item_repository = item_repository
        self.member_repository = member_repository
        self.organization_repository = organization_repository
        self.joined_organization_repository = joined_organization_repository

    async def create_item(self, db:Session, me_dto:MemberDTO, create_item_dto:CreateItemDto):
        me = await self.member_repository.find_by_id(db, me_dto.id)
        if me is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        organization:Optional[Organization] = await self.organization_repository.find_by_id(db, create_item_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        category = await self.category_repository.find_category_by_id(db, create_item_dto.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        joined_organization:JoinedOrganization = await self.joined_organization_repository.find_by_member_and_organization(db, me, organization)
        if joined_organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if joined_organization.member_role not in [MemberRole.READ_WRITE, MemberRole.ADMIN, MemberRole.OWNER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Member not found")

        await self.item_repository.create_item(
            db,
            create_item_dto.item_name,
            organization,
            category,
            create_item_dto.year
        )

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK
from common.dependency_injector import Container
from common.security.member_DTO import MemberDTO
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.service import ItemService

router = APIRouter(prefix="/ledger/item", tags=["Item"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_item(
        request: Request,
        response: Response,
        create_item_dto:CreateItemDto,
        db: Session = Depends(get_db),
        item_service: ItemService = Depends(Provide[Container.item_service])
):
    me_dto: MemberDTO = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_item_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await item_service.create_item(db, create_item_dto)


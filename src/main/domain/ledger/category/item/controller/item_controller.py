from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from common.security.member_DTO import MemberDTO
from common.security.rq import get_current_user_from_cookie
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.service import ItemService

router = APIRouter(prefix="/ledger/item", tags=["Item"])

@router.post("/")
@inject
async def create_item(
        request: Request,
        response: Response,
        create_item_dto:CreateItemDto,
        db: Session = Depends(get_db),
        item_service: ItemService = Depends(Provide[Container.item_service])
):
    try:
        me_dto: MemberDTO = await get_current_user_from_cookie(request, response, db)
        await item_service.create_item(db, me_dto, create_item_dto)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err


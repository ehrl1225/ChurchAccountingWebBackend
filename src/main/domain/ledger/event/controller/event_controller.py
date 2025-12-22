from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.service import EventService

router = APIRouter(prefix="/ledger/event", tags=["Event"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
        request:Request,
        response:Response,
        create_event_dto:CreateEventDTO,
        db:Session = Depends(get_db),
        event_service:EventService = Depends(Provide[Container.event_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_event_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await event_service.create_event(db, create_event_dto)


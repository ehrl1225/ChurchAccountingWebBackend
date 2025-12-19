from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.service import EventService

router = APIRouter(prefix="/ledger/event")

@router.post("/", tags=["event"])
async def create_event(
        request:Request,
        response:Response,
        create_event_dto:CreateEventDTO,
        db:Session = Depends(get_db),
        event_service:EventService = Depends(Provide[Container.event_service])
):
    try:
        me_dto = get_current_user_from_cookie(request, response, db)
        await event_service.create_event(db, me_dto, create_event_dto)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err


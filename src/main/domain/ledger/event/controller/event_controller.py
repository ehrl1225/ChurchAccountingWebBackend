from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.delete_event_params import DeleteEventParams
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.ledger.event.dto.search_event_params import SearchEventParams
from domain.ledger.event.service import EventService

router = APIRouter(prefix="/ledger/event", tags=["Event"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_event(
        request:Request,
        response:Response,
        create_event_dto:CreateEventDTO,
        db: AsyncSession = Depends(get_db),
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

@router.get("/")
@inject
async def get_events(
        request:Request,
        response:Response,
        params: Annotated[SearchEventParams, Depends()],
        db: AsyncSession = Depends(get_db),
        event_service:EventService = Depends(Provide[Container.event_service])
):
    if params.organization_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if params.year is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=params.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    return await event_service.find_all(db, params)

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def update_event(
        request:Request,
        response:Response,
        edit_event_dto:EditEventDto,
        db: AsyncSession = Depends(get_db),
        event_service:EventService = Depends(Provide[Container.event_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_event_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await event_service.update(db, edit_event_dto)

@router.delete("/")
@inject
async def delete_event(
        request:Request,
        response:Response,
        delete_event_params:Annotated[DeleteEventParams, Depends()],
        db: AsyncSession = Depends(get_db),
        event_service:EventService = Depends(Provide[Container.event_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=delete_event_params.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await event_service.delete(db, delete_event_params)

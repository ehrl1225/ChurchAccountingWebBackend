from typing import Literal, List
import asyncio
import json
import hashlib

from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from common.database.member_role import OWNER2ADMIN_MASK
from common.dependency_injector import Container
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto
from domain.organization.organization_invitation.entity import StatusEnum
from domain.organization.organization_invitation.service import OrganizationInvitationService
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.organization.organization_invitation.dto import OrganizationInvitationResponseDto

router = APIRouter(prefix="/organization-invitation", tags=["Organization Invitation"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_organization_invitation(
        request: Request,
        response: Response,
        organization_invitation_dto: CreateOrganizationInvitationDto,
        db: AsyncSession = Depends(get_db),
        organization_invitation_service:OrganizationInvitationService =  Depends(Provide[Container.organization_invitation_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    if organization_invitation_dto.email == me_dto.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=organization_invitation_dto.organization_id,
        member_role_mask=OWNER2ADMIN_MASK
    )
    await organization_invitation_service.create(db, me_dto, organization_invitation_dto)

@router.put("/{organization_invitation_id}/{status}", status_code=status.HTTP_200_OK)
@inject
async def update_organization_invitation(
        request: Request,
        response: Response,
        organization_invitation_id: int,
        status_literal: Literal["accept", "reject"],
        db: AsyncSession = Depends(get_db),
        organization_invitation_service: OrganizationInvitationService = Depends(Provide[Container.organization_invitation_service])
):
    me = await get_current_user_from_cookie(request, response, db)
    status_enum = StatusEnum.PENDING
    match status_literal:
        case "accept":
            status_enum = StatusEnum.ACCEPTED
        case "reject":
            status_enum = StatusEnum.REJECTED
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await organization_invitation_service.update(db, me, organization_invitation_id, status_enum)

@router.get("/", response_model=List[OrganizationInvitationResponseDto])
@inject
async def get_organization_invitations(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        organization_invitation_service:OrganizationInvitationService = Depends(Provide[Container.organization_invitation_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    organization_invitations = await organization_invitation_service.get_invitations(db, me_dto)
    return organization_invitations

@router.get("/subscribe")
@inject
async def subscribe_to_invitations(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        organization_invitation_service: OrganizationInvitationService = Depends(
            Provide[Container.organization_invitation_service]
        ),
):
    me_dto = await get_current_user_from_cookie(request, response, db)

    async def event_generator(request: Request):
        last_hash = ""
        while True:
            if await request.is_disconnected():
                break
            invitations = await organization_invitation_service.get_invitations(db, me_dto)

            sorted_invitations = sorted(invitations, key=lambda inv: inv.id)
            invitation_json_for_hash = json.dumps([inv.model_dump() for inv in sorted_invitations])
            current_hash = hashlib.sha256(invitation_json_for_hash.encode("utf-8")).hexdigest()

            if current_hash != last_hash:
                response_data = [inv.model_dump() for inv in invitations]
                yield f"data: {json.dumps(response_data)}\n\n"
                last_hash = current_hash
            await asyncio.sleep(5)
    return StreamingResponse(event_generator(request), media_type="text/event-stream")
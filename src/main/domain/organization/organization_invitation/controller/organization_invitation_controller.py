from typing import Literal, List
import json

from fastapi import APIRouter, Request, Response, Depends, status, HTTPException, BackgroundTasks
from dependency_injector.wiring import inject, Provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from common.database import get_db, SessionLocal
from common.enum.member_role import OWNER2ADMIN_MASK
from common.enum.status_enum import StatusEnum
from common.dependency_injector import Container
from common.redis import get_redis
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto
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
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis),
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
    invitation = await organization_invitation_service.create(db, me_dto, organization_invitation_dto)
    async def publish_invitation(member_id:int):
        channel = f"invitations:{member_id}"
        await redis.publish(channel, "Invitation created")
    background_tasks.add_task(publish_invitation, invitation.member_id)

@router.put("/{organization_invitation_id}/{status}", status_code=status.HTTP_200_OK)
@inject
async def update_organization_invitation(
        request: Request,
        response: Response,
        organization_invitation_id: int,
        status_literal: Literal["accept", "reject"],
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis),
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
    async def publish_invitation():
        channel = f"invitations:{me.id}"
        await redis.publish(channel, "Invitation modified")
    background_tasks.add_task(publish_invitation)

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
        redis_client: Redis = Depends(get_redis),
        organization_invitation_service: OrganizationInvitationService = Depends(
            Provide[Container.organization_invitation_service]
        ),
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    channel = f"invitations:{me_dto.id}"

    async def event_generator():
        async with redis_client.pubsub() as pubsub:
            await pubsub.subscribe(channel)
            while True:
                if await request.is_disconnected():
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=60)
                if message:
                    invitations = await organization_invitation_service.get_invitations(db, me_dto)
                    response_data = [invitation.model_dump() for invitation in invitations]
                    json_response = json.dumps(response_data)
                    yield {"data": json_response}
    return EventSourceResponse(event_generator())
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db, MemberRole
from common.database.member_role import OWNER2ADMIN_MASK, OWNER2READ_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.organization.joined_organization.dto import ChangeRoleDto
from domain.organization.joined_organization.dto.delete_joined_organization_params import DeleteJoinedOrganizationParams
from domain.organization.joined_organization.service import JoinedOrganizationService
from domain.organization.organization.dto import OrganizationResponseDto

router = APIRouter(prefix="/joined-organization", tags=["joined-organization"])

@router.put("/{organization_id}", status_code=status.HTTP_200_OK)
@inject
async def change_role(
        request: Request,
        response: Response,
        organization_id: int,
        change_role: ChangeRoleDto,
        db: AsyncSession = Depends(get_db),
        joined_organization_service:JoinedOrganizationService =  Depends(Provide[Container.joined_organization_service])
):
    if change_role.member_role == MemberRole.OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=organization_id,
        member_role_mask=OWNER2ADMIN_MASK,
    )
    if (await joined_organization_service.check_if_owner(
            db=db,
            organization_id=organization_id,
            member_id=me_dto.id)
            and change_role.member_id == me_dto.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await joined_organization_service.change_member_role(db, organization_id, change_role)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrganizationResponseDto])
@inject
async def list_joined_organizations(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        joined_organization_service: JoinedOrganizationService = Depends(Provide[Container.joined_organization_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    result = await joined_organization_service.get_all_joined_organizations(db, me_dto)
    return result

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_joined_organization(
        request: Request,
        response: Response,
        delete_joined_organization: Annotated[DeleteJoinedOrganizationParams, Depends()],
        db: AsyncSession = Depends(get_db),
        joined_organization_service:JoinedOrganizationService = Depends(Provide[Container.joined_organization_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=delete_joined_organization.organization_id,
        member_role_mask=OWNER2ADMIN_MASK,
    )
    await joined_organization_service.delete_joined_organization(db, delete_joined_organization)

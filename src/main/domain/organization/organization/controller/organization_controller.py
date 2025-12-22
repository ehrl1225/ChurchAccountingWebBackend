from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide

from common.database.member_role import OWNER_ONLY_MASK
from common.dependency_injector import Container
from common.database import get_db
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.organization.organization.service import OrganizationService
from domain.organization.organization.dto import OrganizationCreateDto

router = APIRouter(prefix="/organization", tags=["organization"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_organization(
        organization:OrganizationCreateDto,
        request:Request,
        response:Response,
        db:Session = Depends(get_db),
        organization_service:OrganizationService = Depends(Provide[Container.organization_service])
):
    member = await get_current_user_from_cookie(request, response, db)
    await organization_service.create(db, member, organization)

@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_organization(
        request:Request,
        response:Response,
        organization_id: int,
        db:Session = Depends(get_db),
        organization_service:OrganizationService = Depends(Provide[Container.organization_service]),
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(db, me_dto.id, organization_id, OWNER_ONLY_MASK)
    await organization_service.delete(db, organization_id)
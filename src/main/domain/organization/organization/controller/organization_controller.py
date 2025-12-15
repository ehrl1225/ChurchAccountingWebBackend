from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide

from common.dependency_injector import Container
from common.database import get_db
from common.security.rq import get_current_user_from_cookie
from domain.organization.organization.service import OrganizationService
from domain.organization.organization.dto import OrganizationCreateDto

router = APIRouter(prefix="/organization", tags=["organization"])

@router.post("/")
@inject
async def create_organization(
        organization:OrganizationCreateDto,
        request:Request,
        response:Response,
        db:Session = Depends(get_db),
        organization_service:OrganizationService = Depends(Provide[Container.organization_service])
):
    member = get_current_user_from_cookie(request, response, db)
    organization = await organization_service.create(db, member, organization)


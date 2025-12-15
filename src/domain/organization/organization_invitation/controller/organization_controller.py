from fastapi import APIRouter, Request, Response, Depends
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto
from domain.organization.organization_invitation.service import OrganizationInvitationService
from common.security.rq import get_current_user_from_cookie

router = APIRouter(prefix="/organization/invitation", tags=["Organization Invitation"])

@router.post("/")
@inject
async def create_organization_invitation(
        request: Request,
        response: Response,
        organization_invitation_dto: CreateOrganizationInvitationDto,
        db: Session = Depends(get_db),
        organization_invitation_service:OrganizationInvitationService =  Depends(Provide[Container.organization_invitation_service])
):
    try:
        member = get_current_user_from_cookie(request, response, db)
        await organization_invitation_service.create(db, member, organization_invitation_dto)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

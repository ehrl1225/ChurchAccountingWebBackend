from dependency_injector.wiring import inject
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session

from common.database import get_db
from common.security.rq import get_current_user_from_cookie

router = APIRouter(prefix="/joined-organization", tags=["joined-organization"])

@router.put("/{organization_id}")
@inject
async def change_role(
        request: Request,
        response: Response,
        organization_id: int,
        db: Session = Depends(get_db)
):
    me_dto = await get_current_user_from_cookie(request, response, db)

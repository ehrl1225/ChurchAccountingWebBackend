from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.service import ReceiptService

router = APIRouter(prefix="/ledger/receipt", tags=["receipt"])


@router.post("/ledger/receipt", status_code=status.HTTP_201_CREATED)
@inject
async def create_receipt(
        request: Request,
        response: Response,
        create_receipt_dto: CreateReceiptDto,
        db:Session = Depends(get_db),
        receipt_service:ReceiptService =  Depends(Provide[Container.receipt_service])
):
    try:
        me_dto = await get_current_user_from_cookie(request, response, db)
        await check_member_role(
            db=db,
            member_id=me_dto.id,
            organization_id=create_receipt_dto.organization_id,
            member_role_mask=OWNER2READ_WRITE_MASK
        )
        await receipt_service.create_receipt(db, create_receipt_dto)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
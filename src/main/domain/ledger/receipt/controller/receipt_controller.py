from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.service import ReceiptService

router = APIRouter(prefix="/ledger/receipt", tags=["receipt"])


@router.post("/ledger/receipt", tags=["receipt"])
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
        await receipt_service.create_receipt(db, me_dto, create_receipt_dto)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
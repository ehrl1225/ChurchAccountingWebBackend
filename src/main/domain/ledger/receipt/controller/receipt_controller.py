from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session
from typing import Annotated

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.delete_receipt_params import DeleteReceiptParams
from domain.ledger.receipt.dto.edit_receipt_dto import EditReceiptDto
from domain.ledger.receipt.dto.search_receipt_params import SearchAllReceiptParams
from domain.ledger.receipt.service import ReceiptService

router = APIRouter(prefix="/ledger/receipt", tags=["receipt"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_receipt(
        request: Request,
        response: Response,
        create_receipt_dto: CreateReceiptDto,
        db:Session = Depends(get_db),
        receipt_service:ReceiptService =  Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_receipt_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await receipt_service.create_receipt(db, create_receipt_dto)

@router.get("/all")
@inject
async def get_all_receipts(
        request: Request,
        response: Response,
        params: Annotated[SearchAllReceiptParams, Depends()],
        db:Session = Depends(get_db),
        receipt_service:ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=params.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    return await receipt_service.get_all_receipts(db, params)

@router.get("/summary")
async def get_summary_receipts(
        request: Request,
        response: Response,
):
    pass

@router.put("/")
@inject
async def update_receipt(
        request: Request,
        response: Response,
        edit_receipt_dto: EditReceiptDto,
        db:Session = Depends(get_db),
        receipt_service: ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_receipt_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await receipt_service.update(db, edit_receipt_dto)

@router.delete("/")
@inject
async def delete_receipt(
        request: Request,
        response: Response,
        delete_receipt_params: Annotated[DeleteReceiptParams, Depends()],
        db:Session = Depends(get_db),
        receipt_service: ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=delete_receipt_params.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await receipt_service.delete(db, delete_receipt_params)
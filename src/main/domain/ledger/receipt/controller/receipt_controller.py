from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response, status, UploadFile, File
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from common.database.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.request.delete_receipt_params import DeleteReceiptParams
from domain.ledger.receipt.dto.request.edit_receipt_dto import EditReceiptDto
from domain.ledger.receipt.dto.request.search_receipt_params import SearchAllReceiptParams
from domain.ledger.receipt.dto.request.receipt_summary_params import ReceiptSummaryParams
from domain.ledger.receipt.dto.request.upload_receipt_dto import UploadReceiptDto
from domain.ledger.receipt.service import ReceiptService, receipt_service

router = APIRouter(prefix="/ledger/receipt", tags=["receipt"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_receipt(
        request: Request,
        response: Response,
        create_receipt_dto: CreateReceiptDto,
        db: AsyncSession = Depends(get_db),
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

@router.post("/upload")
@inject
async def upload_receipt_excel(
        request: Request,
        response: Response,
        upload_receipt_dto: UploadReceiptDto,
        db: AsyncSession = Depends(get_db),
        receipt_service:ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=upload_receipt_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await receipt_service.upload_excel(upload_receipt_dto)

@router.get("/download/{organization_id}/{year}")
@inject
async def download_receipt_excel(
        request: Request,
        response: Response,
        organization_id: int,
        year: int,
        db: AsyncSession=  Depends(get_db),
        receipt_service:ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    await receipt_service.download_excel(organization_id, year)


@router.get("/all")
@inject
async def get_all_receipts(
        request: Request,
        response: Response,
        params: Annotated[SearchAllReceiptParams, Depends()],
        db: AsyncSession = Depends(get_db),
        receipt_service:ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=params.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    data = await receipt_service.get_all_receipts(db, params)
    return data

@router.get("/summary")
@inject
async def get_summary_receipts(
        request: Request,
        response: Response,
        params: Annotated[ReceiptSummaryParams, Depends()],
        db: AsyncSession = Depends(get_db),
        receipt_service: ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=params.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    return await receipt_service.get_summary_receipt(db, params)

@router.put("/")
@inject
async def update_receipt(
        request: Request,
        response: Response,
        edit_receipt_dto: EditReceiptDto,
        db: AsyncSession = Depends(get_db),
        receipt_service: ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_receipt_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    data = await receipt_service.update(db, edit_receipt_dto)
    return data

@router.delete("/")
@inject
async def delete_receipt(
        request: Request,
        response: Response,
        delete_receipt_params: Annotated[DeleteReceiptParams, Depends()],
        db: AsyncSession = Depends(get_db),
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
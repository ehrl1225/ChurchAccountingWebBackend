import asyncio
import json

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response, status, UploadFile, File
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from sse_starlette import EventSourceResponse

from common.database import get_db
from common.enum.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.request.delete_receipt_params import DeleteReceiptParams
from domain.ledger.receipt.dto.request.download_receipt_image_dto import DownloadReceiptImageDto
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
    return await receipt_service.create_receipt(db, create_receipt_dto)

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

@router.post("/upload/excel")
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

@router.get("/upload/excel/subscribe/{file_name}")
@inject
async def upload_receipt_subscribe(
        request: Request,
        file_name: str,
        redis: Redis = Depends(Provide[Container.redis_client]),
):
    async def event_generator():
        initial_result = await redis.get(f"file_name:{file_name}")
        if initial_result:
            data = json.loads(initial_result)
            if data["status"] in ["completed", "failed"]:
                yield {"event": "job_update", "data": initial_result}
                return
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"excel_upload:{file_name}")
        try:
            while True:
                if await request.is_disconnected():
                    await pubsub.unsubscribe(f"excel_upload:{file_name}")
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    final_result = await redis.get(f"file_name:{file_name}")
                    if final_result:
                        yield {"event": "job_update", "data": final_result}
                        break
                yield {"event": "ping", "data": "pong"}
        except asyncio.CancelledError:
            await pubsub.unsubscribe(f"excel_upload:{file_name}")
            raise
    return EventSourceResponse(event_generator())

@router.post("/download/excel/{organization_id}/{year}")
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
    data = await receipt_service.download_excel(organization_id, year)
    return data


@router.get("/download/excel/subscribe/{file_name}", summary="엑셀 다운로드 작업 상태 실시간 구도게")
@inject
async def download_receipt_subscribe(
        request: Request,
        file_name: str,
        redis: Redis = Depends(Provide[Container.redis_client])
):
    async def event_generator():
        initial_result = await redis.get(f"file_name:{file_name}")
        if initial_result:
            data = json.loads(initial_result)
            if data["status"] in ["completed", "failed"]:
                yield {"event": "job_update", "data": initial_result}
                return
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"excel_download:{file_name}")
        try:
            while True:
                if await request.is_disconnected():
                    await pubsub.unsubscribe(f"excel_download:{file_name}")
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    final_result = await redis.get(f"file_name:{file_name}")
                    if final_result:
                        yield {"event": "job_update", "data": final_result}
                        break
                yield {"event": "ping", "data": "ping"}
        except asyncio.CancelledError:
            await pubsub.unsubscribe(f"excel_download:{file_name}")
            raise
    return EventSourceResponse(event_generator())

@router.post("/download/image")
@inject
async def download_receipt_image(
        request: Request,
        response: Response,
        download_receipt_image_dto:DownloadReceiptImageDto,
        db: AsyncSession = Depends(get_db),
        receipt_service:ReceiptService = Depends(Provide[Container.receipt_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=download_receipt_image_dto.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    data = await receipt_service.download_receipt_images(db, download_receipt_image_dto)
    return data

@router.get("/download/image/subscribe/{file_name}")
@inject
async def download_receipt_image_subscribe(
        request: Request,
        file_name: str,
        redis: Redis = Depends(Provide[Container.redis_client])
):
    async def event_generator():
        initial_result = await redis.get(f"receipt_image_zip:{file_name}")
        if initial_result:
            data = json.loads(initial_result)
            if data["status"] in ["completed", "failed"]:
                yield {"event": "job_update", "data":initial_result}
                return
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"receipt_image_download:{file_name}")
        try:
            while True:
                if await request.is_disconnected():
                    await pubsub.unsubscribe("receipt_image_download:{file_name}")
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    final_result = await redis.get(f"receipt_image_zip:{file_name}")
                    if final_result:
                        yield {"event": "job_update", "data":final_result}
                        break
                yield {"event": "ping", "data": "ping"}
        except asyncio.CancelledError:
            await pubsub.unsubscribe("receipt_image_download:{file_name}")
            raise

    return EventSourceResponse(event_generator())
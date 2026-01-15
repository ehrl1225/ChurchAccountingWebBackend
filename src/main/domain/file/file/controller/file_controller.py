from fastapi import APIRouter, Depends, Request, Response
from dependency_injector.wiring import inject, Provide
import pathlib
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from common.database.member_role import OWNER2READ_MASK, OWNER2READ_WRITE_MASK
from common.security.rq import get_current_user_from_cookie, check_member_role
from common.dependency_injector import Container
from domain.file.file.dto import CreateFileInfo
from domain.file.file.dto.file_info_response_dto import FileInfoResponseDto
from domain.file.file.service import StorageService, FileService

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/url/post/")
@inject
async def get_presigned_post_url(
        request: Request,
        response: Response,
        create_file_info: CreateFileInfo,
        db: AsyncSession = Depends(get_db),
        file_service: FileService = Depends(Provide[Container.file_service]),
        storage_service: StorageService = Depends(Provide[Container.storage_service]),
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_file_info.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    ext = pathlib.Path(create_file_info.file_name).suffix
    file_name = f"{uuid.uuid4().hex}{ext}"
    object_name = f"receipt/{create_file_info.organization_id}/{file_name}"
    file_info = await file_service.create_file_info(db, create_file_info, file_name)
    url = await storage_service.create_presigned_post_url(object_name)
    return FileInfoResponseDto(
        id=file_info.id,
        file_name=file_name,
        url=url,
    )

@router.get("/url/get/{organization_id}/{file_name:path}")
@inject
async def get_presigned_get_url(
        request: Request,
        response: Response,
        organization_id: int,
        file_name: str,
        db: AsyncSession = Depends(get_db),
        storage_service: StorageService = Depends(Provide[Container.storage_service]),
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=organization_id,
        member_role_mask=OWNER2READ_MASK,
    )
    object_name = f"/receipt/{organization_id}/{file_name}"
    url =await storage_service.create_presigned_get_url(object_name)

    return FileInfoResponseDto(
        id=0,
        file_name=file_name,
        url=url,
    )


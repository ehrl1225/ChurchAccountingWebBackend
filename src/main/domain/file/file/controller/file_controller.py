from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
import pathlib
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from domain.file.file.service import StorageService, FileService

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def upload_file(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        storage_service: StorageService = Depends(Provide[Container.storage_service]),
        file_service: FileService = Depends(Provide[Container.file_service])
):
    ext = pathlib.Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    await file_service.create_file_info(db, file, filename, await storage_service.get_file_url(filename))
    await storage_service.upload_file(file.file, filename, file.content_type)



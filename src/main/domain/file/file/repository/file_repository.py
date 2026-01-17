from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.file.file.dto import CreateFileInfo
from domain.file.file.entity import FileInfo

class FileRepository:


    async def create_file_info(self, db:AsyncSession, create_file_info:CreateFileInfo, file_name:str):
        file_info = FileInfo(
            file_name=file_name,
            organization_id=create_file_info.organization_id,
            uploaded_at=datetime.now(),
        )
        db.add(file_info)
        await db.flush()
        await db.refresh(file_info)
        return file_info

    async def has_file(self, db:AsyncSession, organization_id: int, file_name: str) -> bool:
        query = (
            select(FileInfo)
                .filter(FileInfo.organization_id == organization_id)
                .filter(FileInfo.original_file_name == file_name)
        )
        result = await db.execute(query)
        file_info = result.scalar_one_or_none()
        return file_info is not None

    async def find_by_id(self, db:AsyncSession, file_id: int) -> Optional[FileInfo]:
        return await db.get(FileInfo, file_id)

    async def find_by_receipt_id(self, db:AsyncSession, receipt_id: int) -> Optional[FileInfo]:
        query = (
            select(FileInfo)
            .filter(FileInfo.receipt_id == receipt_id)
        )
        result = await db.execute(query)
        file_info = result.scalar_one_or_none()
        return file_info

    async def update_file_info(self, db:AsyncSession, file_info:FileInfo, receipt_id:Optional[int]):
        file_info.receipt_id = receipt_id
        await db.flush()
        await db.refresh(file_info)
        return file_info
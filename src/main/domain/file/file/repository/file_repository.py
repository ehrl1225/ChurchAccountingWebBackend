from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from domain.file.file.entity import FileInfo

class FileRepository:


    async def create_file_info(self, db:AsyncSession, file: UploadFile, file_name: str, file_url: str):
        file_info = FileInfo(
            file_name=file_name,
            original_file_name=file.filename,
            content_type=file.content_type,
            file_size=file.size,
            file_url=file_url
        )
        await db.add(file_info)
        await db.flush()
        await db.refresh(file_info)

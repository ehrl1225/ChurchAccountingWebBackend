from sqlalchemy.ext.asyncio import AsyncSession

from domain.file.file.dto import CreateFileInfo
from domain.file.file.entity import FileInfo
from domain.file.file.repository import FileRepository


class FileService:

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def create_file_info(self, db:AsyncSession, create_file_info:CreateFileInfo, object_name:str)->FileInfo:
        return await self.file_repository.create_file_info(db, create_file_info, object_name)


from fastapi import UploadFile
from sqlalchemy.orm import Session

from domain.file.file.repository import FileRepository
from domain.file.file.entity import FileInfo

class FileService:

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def create_file_info(self, db:Session, file: UploadFile, file_name:str, file_url:str):
        file_info = await self.file_repository.create_file_info(db, file, file_name, file_url)
        return file_info

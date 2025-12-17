from fastapi import UploadFile
from sqlalchemy.orm import Session

from domain.file.file.entity import FileInfo

class FileRepository:


    async def create_file_info(self, db:Session, file: UploadFile, file_name: str, file_url: str):
        file_info = FileInfo(
            file_name=file_name,
            original_file_name=file.filename,
            content_type=file.content_type,
            file_size=file.size,
            file_url=file_url
        )
        db.add(file_info)
        db.flush()
        db.refresh(file_info)

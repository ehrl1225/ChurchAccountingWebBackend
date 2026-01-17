from typing import Optional

from pydantic import BaseModel

class FileInfoResponseDto(BaseModel):
    id: int
    file_name: str
    url: str
    fields: dict[str, str] = dict()
from pydantic import BaseModel

class FileInfoPost(BaseModel):
    url: str
    fields: dict[str, str] = dict()
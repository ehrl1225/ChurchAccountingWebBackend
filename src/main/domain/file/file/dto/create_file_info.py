from pydantic import BaseModel

class CreateFileInfo(BaseModel):
    organization_id: int
    year: int
    file_name: str
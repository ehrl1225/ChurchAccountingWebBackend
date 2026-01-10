from pydantic import BaseModel

class UploadExcelDto(BaseModel):
    organization_id: int
    year: int
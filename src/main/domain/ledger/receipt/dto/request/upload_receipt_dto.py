from pydantic import BaseModel

class UploadReceiptDto(BaseModel):
    organization_id: int
    year:int
    excel_file_name: str
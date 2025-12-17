import requests
from typing import BinaryIO

from src.main.domain.file.file.service import StorageService
from fastapi import HTTPException, status

FILE_SERVER_URL: str = "http://localhost:8001"

class LocalStorageService(StorageService):
    async def upload_file(self, file: BinaryIO, file_name: str, content_type: str) -> str:
        files = {"file": (file_name, file, content_type)}
        try:
            response = requests.post(f"{FILE_SERVER_URL}/file", files=files, timeout=5)
            response.raise_for_status()

            response_json = response.json()
            if "image_url" not in response_json:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            return response_json["image_url"]
        except requests.exceptions.RequestException as err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Could not communicate with file server: {err}"
            )
        finally:
            file.close()

    async def get_file_url(self, file_name: str) -> str:
        return f"{FILE_SERVER_URL}/uploads/{file_name}"

    async def delete_file(self, file_name: str) -> str:
        try:
            delete_url = f"{FILE_SERVER_URL}/file/{file_name}"
            response = requests.delete(delete_url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Could not communicate with file server : {err}"
            )
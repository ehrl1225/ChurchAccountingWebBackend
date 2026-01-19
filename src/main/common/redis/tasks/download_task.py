import pandas as pd
import httpx
import asyncio
from typing import Optional

from common.env import settings
from domain.file.file.service import StorageService, S3StorageService, LocalStorageService


async def async_process_excel():
    storage_service: Optional[StorageService] = None
    match settings.PROFILE:
        case "prod":
            storage_service = S3StorageService()
        case _:
            storage_service = LocalStorageService()


def process_excel_receipt_download(file_path: str, organization_id: int, year: int):
    asyncio.run(async_process_excel())
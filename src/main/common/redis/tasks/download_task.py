import io
import json

import pandas as pd
import httpx
import asyncio
from typing import Optional

from common.database import SessionLocal
from common.database.file_type import FileType
from common.redis.redis_client import RedisClient
from common.redis import get_redis
from common.env import settings
from domain.file.file.service import StorageService, S3StorageService, LocalStorageService
from domain.ledger.receipt.repository import ReceiptRepository

async def async_process_excel(file_name: str, organization_id: int, year: int):
    await RedisClient.init()
    file_path = f"{FileType.EXCEL.value}/{organization_id}/{year}/{file_name}"
    receipt_repository = ReceiptRepository()
    redis = await get_redis()
    storage_service: Optional[StorageService] = None
    match settings.PROFILE:
        case "prod":
            storage_service = S3StorageService()
        case _:
            storage_service = LocalStorageService()
    print("Processing excel receipt download")
    result_payload = {}
    async with SessionLocal() as db:
        try:
            receipts = await receipt_repository.find_all(
                db,
                organization_id=organization_id,
                year=year,
            )
            data = [
                {
                    "paper_date": receipt.paper_date,
                    "actual_date" : receipt.actual_date,
                    "name" : receipt.name,
                    "amount" : receipt.amount,
                    "category_name" : receipt.category.name,
                    "item_name" : receipt.item.name,
                    "event_name" : receipt.event.name if receipt.event_id is not None else None,
                    "etc" : receipt.etc
                } for receipt in receipts
            ]
            df = pd.DataFrame(data)

            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)

            async with httpx.AsyncClient() as client:
                file_post_url = await storage_service.create_presigned_post_url(file_path)
                if file_post_url is None:
                    raise Exception("Failed to create presigned post url")
                files = {"file": excel_buffer}
                response = await client.post(file_post_url.url, files=files, data=file_post_url.fields)
                response.raise_for_status()
                file_get_url = await storage_service.create_presigned_get_url(file_path)

                result_payload = {"status":"completed", "file_url":file_get_url}
                print(f"Completed receipt download: {file_path}")

        except Exception as e:
            print("failed")
            print(e)
            result_payload = {"status":"failed", "file_url":file_path}
            await db.rollback()

        finally:
            if result_payload:
                await redis.set(f"file_name:{file_name}", json.dumps(result_payload), ex=600)
            channel_name = f"excel_download:{file_name}"
            await redis.publish(channel_name, "completed")
            await RedisClient.close()


def process_excel_receipt_download(file_name: str, organization_id: int, year: int):
    asyncio.run(async_process_excel(file_name, organization_id, year))
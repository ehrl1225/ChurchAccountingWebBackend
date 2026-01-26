import asyncio
from typing import Optional
import httpx
import io
import zipfile
import json

from common.database import SessionLocal
from common.enum.file_type import FileType
from common.enum.summary_type import SummaryType
from common.redis.redis_client import RedisClient
from common.redis import get_redis
from common.env import settings
from domain.file.file.entity import FileInfo
from domain.organization.organization.entity import Organization
from domain.organization.organization_invitation.entity import OrganizationInvitation
from domain.organization.joined_organization.entity import JoinedOrganization
from domain.ledger.event.entity import Event
from domain.member.entity import Member
from domain.file.file.service import StorageService, S3StorageService, LocalStorageService
from domain.ledger.receipt.repository import ReceiptRepository

async def async_process_receipt(
        file_name:str,
        summary_type:str,
        organization_id:int,
        year:int,
        month:Optional[int]=None,
        event_id:Optional[int]=None,
):
    await RedisClient.init()
    redis = await get_redis()
    receipt_repository = ReceiptRepository()
    storage_service: Optional[StorageService] = None
    match settings.PROFILE:
        case "prod":
            storage_service = S3StorageService()
        case _:
            storage_service = LocalStorageService()

    file_path = f"{FileType.ZIP.value}/{organization_id}/{year}/{file_name}"

    print("Processing excel receipt download...")
    receipt_image_file_names = []
    async with SessionLocal() as db:
        try:
            if summary_type == SummaryType.MONTH.value:
                if month:
                    receipts = await receipt_repository.find_all_by_month_with_file(db, organization_id, year, month)
                else:
                    receipts = await receipt_repository.find_all(db, organization_id, year)
            elif summary_type == SummaryType.EVENT.value:
                if event_id:
                    receipts = await receipt_repository.find_all_by_event_with_file(db, organization_id, year, event_id)
                else:
                    receipts = await receipt_repository.find_by_event(db, organization_id, year)
            else:
                raise Exception(f"Invalid summary_type: {summary_type}")
            for receipt in receipts:
                file:FileInfo = receipt.file
                if file is None:
                    continue
                receipt_image_file_names.append(file.file_name)
        except Exception as e:
            result_payload = {"status": "failed", "file_url": "no url"}
            raise e
    memory_file = io.BytesIO()
    try:
        with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
            async with httpx.AsyncClient() as client:
                for receipt_image_file_name in receipt_image_file_names:
                    receipt_image_file_path = f"{FileType.RECEIPT.value}/{organization_id}/{year}/{receipt_image_file_name}"
                    url = await storage_service.create_presigned_get_url(receipt_image_file_path)
                    response = await client.get(url)
                    response.raise_for_status()
                    zf.writestr(receipt_image_file_name, response.content)

        memory_file.seek(0)
        async with httpx.AsyncClient() as client:
            upload_url = await storage_service.create_presigned_post_url(file_path)
            files = {"file": memory_file}
            response = await client.post(upload_url.url, files=files, data=upload_url.fields)
            response.raise_for_status()

            download_url = await storage_service.create_presigned_get_url(file_path)
            result_payload = {"status": "completed", "file_url": download_url}
            print(f"Completed receipt image download: {file_path}")

    except Exception as e:
        result_payload = {"status":"failed", "file_url":"no url"}
        memory_file.close()
        raise e

    finally:
        if result_payload:
            await redis.set(f"receipt_image_zip:{file_name}", json.dumps(result_payload), ex=600)
        memory_file.close()
        channel_name = f"receipt_image_download:{file_name}"
        await redis.publish(channel_name, "completed")
        await RedisClient.close()



def process_receipt_image_download(
        file_name:str,
        summary_type: str,
        organization_id:int,
        year:int,
        month:Optional[int]=None,
        event_id:Optional[int]=None,
):
    asyncio.run(async_process_receipt(
        file_name,
        summary_type,
        organization_id,
        year,
        month,
        event_id,
    ))

if __name__ == '__main__':
    process_receipt_image_download(
        "test.zip",
        SummaryType.MONTH.value,
        1,
        2026,
        1,
        None
    )
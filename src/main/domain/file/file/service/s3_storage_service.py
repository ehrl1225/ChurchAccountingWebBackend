import boto3
from boto3.session import Session
from typing import BinaryIO
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from common.env import settings
from domain.file.file.service import StorageService

class S3StorageService(StorageService):

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.REGION_NAME,
        )

    async def upload_file(self, file: BinaryIO, file_name: str, content_type: str) -> str:
        try:
            self.s3_client.upload_fileobj(
                file,
                settings.BUCKET_NAME,
                file_name,
                ExtraArgs={"ContentType": content_type},
            )
        except ClientError as err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Could not communicate with file server: {err}"
            )
        finally:
            file.close()
        return await self.get_file_url(file_name)

    async def get_file_url(self, file_name: str) -> str:
        return f"https://{settings.BUCKET_NAME}.s3.{settings.REGION_NAME}.amazonaws.com/{file_name}"

    async def delete_file(self, file_name: str):
        try:
            self.s3_client.delete_object(
                Bucket=settings.BUCKET_NAME,
                Key=file_name,
            )
        except ClientError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {err}"
            )



import boto3
from typing import BinaryIO, Optional
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from mypy_boto3_s3.client import S3Client

from common.env import settings
from domain.file.file.dto.file_info_post import FileInfoPost
from domain.file.file.service import StorageService

class S3StorageService(StorageService):

    def __init__(self):
        self.s3_client:S3Client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.REGION_NAME,
        )

    async def create_presigned_post_url(self, object_name: str) -> Optional[FileInfoPost]:
        conditions = [
            ["content-length-range", 0, 10 * 1024 * 1024],
        ]
        try:
            response = self.s3_client.generate_presigned_post(
                Bucket=settings.BUCKET_NAME,
                Key=object_name,
                Conditions=conditions,
                ExpiresIn=3600
            )
        except ClientError as err:
            return None
        return FileInfoPost(
            url=response["url"],
            fields=response["fields"],
        )

    async def create_presigned_get_url(self, object_name: str):
        try:
            response = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.BUCKET_NAME,
                        "Key": object_name},
                ExpiresIn=3600)
        except ClientError as err:
            return None
        return response

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



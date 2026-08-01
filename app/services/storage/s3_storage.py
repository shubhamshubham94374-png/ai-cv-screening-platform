import boto3
import uuid
import os
from app.services.storage.base import StorageService


class S3Storage(StorageService):
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region)

    def save(self, file_bytes: bytes, filename: str) -> str:
        ext = os.path.splitext(filename)[1]
        unique_key = f"resumes/{uuid.uuid4()}{ext}"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=unique_key,
            Body=file_bytes,
        )

        return unique_key
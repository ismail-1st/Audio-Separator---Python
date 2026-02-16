import boto3
import os
from boto3.s3.transfer import TransferConfig

STORJ_ACCESS_KEY = os.getenv("STORJ_ACCESS_KEY")
STORJ_SECRET_KEY = os.getenv("STORJ_SECRET_KEY")
STORJ_ENDPOINT = os.getenv("STORJ_ENDPOINT")
STORJ_BUCKET = os.getenv("STORJ_BUCKET")

config = TransferConfig(multipart_threshold=1024 * 1024 * 1000)  # 1000MB


s3 = boto3.client(
    "s3",
    endpoint_url=STORJ_ENDPOINT,
    aws_access_key_id=STORJ_ACCESS_KEY,
    aws_secret_access_key=STORJ_SECRET_KEY,
)

def upload_file(file_path: str, key: str):
    s3.upload_file(file_path, STORJ_BUCKET, key)
    return generate_signed_url(key)


def generate_signed_url(key: str, expires=3600):
    """
    Generate temporary access URL (recommended if bucket is private)
    """
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": STORJ_BUCKET, "Key": key},
        ExpiresIn=expires,
    )

def delete_file(key: str):
    s3.delete_object(Bucket=STORJ_BUCKET, Key=key)
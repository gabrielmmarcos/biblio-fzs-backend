import boto3
from biblio_fzs_backend.settings import Settings


def get_s3_client():
    settings = Settings()

    client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION,
    )

    return client

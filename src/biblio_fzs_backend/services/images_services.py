from http import HTTPStatus

from fastapi import HTTPException, UploadFile

from biblio_fzs_backend.settings import Settings


async def upload_image_to_s3(
    image: UploadFile,
    s3_client,
    filename_with_ext: str,
):
    settings = Settings()

    if not image:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="No image file was uploaded.",
        )

    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

    if image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Unsupported file type",
        )

    image.file.seek(0)

    s3_client.upload_fileobj(
        image.file,
        settings.S3_BUCKET,
        filename_with_ext,
        ExtraArgs={"ContentType": image.content_type},
    )

    image_url = (
        f"https://{settings.S3_BUCKET}.s3.{settings.REGION}.amazonaws.com/"
        f"{filename_with_ext}"
    )

    return {"image_url": image_url}

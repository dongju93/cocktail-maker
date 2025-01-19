from fastapi import UploadFile

MAX_FILE_SIZE: int = 2 * 1024 * 1024
ALLOWED_CONTENT_TYPES: set[str] = {"image/jpeg", "image/png"}


async def is_image_content_type(file: UploadFile | None) -> bool:
    if file is not None and file.content_type not in ALLOWED_CONTENT_TYPES:  # noqa
        return False
    return True


async def is_image_size_too_large(read_file: bytes | None) -> bool:
    if read_file is not None and len(read_file) > MAX_FILE_SIZE:  # noqa
        return False
    return True


async def read_nullable_image(file: UploadFile | None) -> bytes | None:
    return await file.read() if file is not None else None

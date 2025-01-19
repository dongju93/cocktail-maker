from fastapi import UploadFile

MAX_FILE_SIZE = 2 * 1024 * 1024


async def validate_image_extension(file: UploadFile | None) -> bool:
    ALLOWED_CONTENT_TYPES: set[str] = {"image/jpeg", "image/png"}

    if file is not None and file.content_type not in ALLOWED_CONTENT_TYPES:  # noqa
        return False
    return True


async def validate_image_size(read_file: bytes | None) -> bool:
    if read_file is not None and len(read_file) > MAX_FILE_SIZE:  # noqa
        return False
    return True


async def read_image(file: UploadFile | None) -> bytes | None:
    return await file.read() if file is not None else None

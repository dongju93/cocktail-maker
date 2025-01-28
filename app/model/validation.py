from fastapi import UploadFile

from database.query import get_spirits_metadata_from_sqlite
from model.spirits import SpiritsMetadataCategory

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


async def is_metadata_category_valid(
    category: SpiritsMetadataCategory, user_input_metadata: list[str]
) -> bool:
    valid_metadata_list: list[dict[str, str]] = get_spirits_metadata_from_sqlite(
        category
    )
    valid_names: list[str] = [metadata["name"] for metadata in valid_metadata_list]

    return all(
        user_input in valid_names for user_input in user_input_metadata[0].split(",")
    )

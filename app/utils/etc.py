import io
from os import makedirs, path
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from PIL.ImageFile import Image, ImageFile

from model import ResponseFormat, ProblemDetails


async def return_formatter(
    status: Literal["success", "failed"], code: int, data: Any, message: str
) -> ResponseFormat:
    return ResponseFormat(
        status=status,
        code=code,
        data=data,
        message=message,
    )


async def problem_details_formatter(
    status: int,
    title: str,
    detail: str,
    type_uri: str = "about:blank",
    instance: str | None = None,
) -> ProblemDetails:
    """Format error responses according to RFC 9457 Problem Details standard"""
    return ProblemDetails(
        type=type_uri,
        title=title,
        status=status,
        detail=detail,
        instance=instance or f"urn:uuid:{uuid4()}",
    )


def save_image_to_local(image_data: bytes, file_path: Path) -> None:
    # data/images/id 폴더 생성
    makedirs(path.dirname(file_path), exist_ok=True)

    image: ImageFile = Image.open(io.BytesIO(image_data))

    image.save(file_path, "PNG")


def single_word_list_to_many_word_list(
    single_word_list: list[str],
) -> list[str]:
    return single_word_list[0].split(",")

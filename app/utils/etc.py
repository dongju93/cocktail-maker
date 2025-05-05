import io
import os
from pathlib import Path
from typing import Any, Literal

from PIL.ImageFile import Image, ImageFile

from model.response import ResponseFormat


async def return_formatter(
    status: Literal["success", "failed"], code: int, data: Any, message: str
) -> ResponseFormat:
    return ResponseFormat(
        status=status,
        code=code,
        data=data,
        message=message,
    )


def save_image_to_local(image_data: bytes, file_path: Path) -> None:
    # data/images/id 폴더 생성
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image: ImageFile = Image.open(io.BytesIO(image_data))

    image.save(file_path, "PNG")


def single_word_list_to_many_word_list(
    single_word_list: list[str],
) -> list[str]:
    return single_word_list[0].split(",")

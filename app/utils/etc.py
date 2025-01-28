import io
import os
from pathlib import Path
from typing import Any, Literal

from PIL.ImageFile import Image, ImageFile

from model.etc import ResponseFormat


async def return_formatter(
    status: Literal["success", "failed"], code: int, data: Any, message: str
) -> ResponseFormat:
    return ResponseFormat(
        status=status,
        code=code,
        data=data,
        message=message,
    )


def save_image_to_local(image_data: bytes, file_path: Path) -> str:
    # data/images/id 폴더 생성
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image: ImageFile = Image.open(io.BytesIO(image_data))

    image.save(file_path, "PNG")

    return str(file_path)

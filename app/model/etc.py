from typing import Any, Literal, TypedDict


class ResponseFormat(TypedDict):
    status: Literal["success", "failed"]
    code: int
    data: Any
    message: str


class ImageField(TypedDict, total=False):
    main_image: str
    sub_image_1: str
    sub_image_2: str
    sub_image_3: str
    sub_image_4: str

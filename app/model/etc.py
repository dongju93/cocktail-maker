from enum import Enum
from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, Field

METADATA_KIND = Literal["spirits", "liqueur"]


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


class MetadataCategory(str, Enum):
    AROMA = "aroma"
    TASTE = "taste"
    FINISH = "finish"


class MetadataRegister(BaseModel):
    model_config = {"extra": "forbid"}

    names: Annotated[list[str], Field(..., min_length=1)]

from datetime import datetime
from enum import Enum
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, Field


class SpiritsRegister(TypedDict):
    name: str
    aroma: list[str]
    taste: list[str]
    finish: list[str]
    kind: str
    subKind: str
    amount: float
    alcohol: float
    origin_nation: str
    origin_location: str
    description: str
    main_image: NotRequired[str]
    sub_image_1: NotRequired[str | None]
    sub_image_2: NotRequired[str | None]
    sub_image_3: NotRequired[str | None]
    sub_image_4: NotRequired[str | None]
    created_at: datetime
    updated_at: NotRequired[datetime]


class SpiritsSearch(BaseModel):
    model_config = {"extra": "forbid"}

    name: Annotated[
        str | None, Field(min_length=1, description="주류의 이름, 부분 일치")
    ] = None
    aroma: Annotated[
        list[str] | None,
        Field(min_length=1, description="주류의 향, 목록 중 정확한 일치"),
    ] = None
    pageNumber: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    pageSize: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10


class SpiritsMetadataCategory(str, Enum):
    AROMA = "aroma"
    TASTE = "taste"
    FINISH = "finish"


class SpiritsMetadataRegister(BaseModel):
    model_config = {"extra": "forbid"}

    category: Annotated[SpiritsMetadataCategory, Field(..., min_length=1)]
    name: Annotated[list[str], Field(..., min_length=1)]

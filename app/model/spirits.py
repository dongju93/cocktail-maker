from datetime import datetime
from enum import Enum
from typing import Annotated, TypedDict

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
    main_image: bytes
    sub_image1: bytes | None
    sub_image2: bytes | None
    sub_image3: bytes | None
    sub_image4: bytes | None
    created_at: datetime


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


class Category(str, Enum):
    aroma = "aroma"
    taste = "taste"
    finish = "finish"


class SpiritsMetadataRegister(BaseModel):
    model_config = {"extra": "forbid"}

    category: Annotated[Category, Field(..., min_length=1)]
    name: Annotated[list[str], Field(..., min_length=1)]

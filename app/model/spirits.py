from datetime import datetime
from enum import Enum
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, Field

# class SpiritsRegister(BaseModel):
#     model_config = {"extra": "forbid"}

#     name: Annotated[str, Field(..., min_length=1)]
#     aroma: Annotated[list[str], Field(..., min_length=1)]
#     taste: Annotated[list[str], Field(..., min_length=1)]
#     finish: Annotated[list[str], Field(..., min_length=1)]
#     kind: Annotated[str, Field(...)]
#     subKind: Annotated[str, Field(...)]
#     amount: Annotated[float, Field(...)]
#     alcohol: Annotated[float, Field(...)]
#     origin_nation: Annotated[str, Field(...)]
#     origin_location: Annotated[str, Field(...)]
#     description: Annotated[str, Field(...)]


# class SpiritsRegister(BaseModel):
# model_config = {"extra": "forbid"}

# name: Annotated[str, Form(..., min_length=1)]
# aroma: Annotated[list[str], Form(..., min_length=1)]
# taste: Annotated[list[str], Form(..., min_length=1)]
# finish: Annotated[list[str], Form(..., min_length=1)]
# kind: Annotated[str, Form(...)]
# subKind: Annotated[str, Form(...)]
# amount: Annotated[float, Form(...)]
# alcohol: Annotated[float, Form(...)]
# origin_nation: Annotated[str, Form(...)]
# origin_location: Annotated[str, Form(...)]
# description: Annotated[str, Form(...)]
# image: Annotated[str, File(...)]


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

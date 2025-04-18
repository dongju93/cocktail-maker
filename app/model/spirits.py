from datetime import datetime
from enum import Enum
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, Field, constr

from model.etc import ImageField

# class Spirits(BaseModel):
#     """
#     주류 기본 정보 등록/수정 시 사용
#     """

#     model_config = {"extra": "forbid"}

#     name: Annotated[str | None, Field(min_length=1)]
#     aroma: Annotated[
#         list[str] | None, Field(min_items=1, item_type=constr(min_length=1))
#     ]
#     taste: Annotated[
#         list[str] | None, Field(min_items=1, item_type=constr(min_length=1))
#     ]
#     finish: Annotated[
#         list[str] | None, Field(min_items=1, item_type=constr(min_length=1))
#     ]
#     kind: Annotated[str | None, Field(min_length=1)]
#     subKind: Annotated[str | None, Field(min_length=1)]
#     amount: Annotated[float | None, Field(ge=0)]
#     alcohol: Annotated[float | None, Field(ge=0)]
#     origin_nation: Annotated[str | None, Field(min_length=1)]
#     origin_location: Annotated[str | None, Field(min_length=1)]
#     description: Annotated[str | None, Field(min_length=1)]


class SpiritsDict(TypedDict):
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
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]
    image_url: NotRequired[str]
    thumbnail_url: NotRequired[str]


class SpiritsSearch(BaseModel):
    model_config = {"extra": "forbid"}

    name: Annotated[
        str | None, Field(min_length=1, description="주류의 이름, 부분 일치")
    ] = None
    aroma: Annotated[
        list[str] | None,
        Field(min_length=1, description="주류의 향, 목록 중 정확한 일치"),
    ] = None
    taste: Annotated[
        list[str] | None,
        Field(min_length=1, description="주류의 맛, 목록 중 정확한 일치"),
    ] = None
    finish: Annotated[
        list[str] | None,
        Field(min_length=1, description="주류의 여운, 목록 중 정확한 일치"),
    ] = None
    kind: Annotated[
        str | None, Field(min_length=1, description="주류의 종류, 정확한 일치")
    ] = None
    subKind: Annotated[
        str | None, Field(min_length=1, description="주류의 세부 종류, 정확한 일치")
    ] = None
    alcohol_min: Annotated[
        float | None, Field(ge=0, description="주류의 최소 알코올 도수")
    ] = None
    alcohol_max: Annotated[
        float | None, Field(ge=0, description="주류의 최대 알코올 도수")
    ] = None
    origin_nation: Annotated[
        str | None, Field(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    origin_location: Annotated[
        str | None, Field(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    pageNumber: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    pageSize: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10


class SpiritsMetadataCategory(str, Enum):
    AROMA = "aroma"
    TASTE = "taste"
    FINISH = "finish"


class SpiritsMetadataRegister(BaseModel):
    model_config = {"extra": "forbid"}

    name: Annotated[list[str], Field(..., min_length=1)]

from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SpiritsRegister(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[str, Field(..., min_length=1)]
    aroma: Annotated[list[str], Field(..., min_length=1)]
    taste: Annotated[list[str], Field(..., min_length=1)]
    finish: Annotated[list[str], Field(..., min_length=1)]
    kind: Annotated[str, Field(...)]
    sub_kind: Annotated[str, Field(...)]
    amount: Annotated[float, Field(...)]
    alcohol: Annotated[float, Field(...)]
    origin_nation: Annotated[str, Field(...)]
    origin_location: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]
    main_image: Annotated[
        UploadFile,
        File(..., description="주류의 대표 이미지, 최대 2MB"),
    ]
    sub_image1: Annotated[UploadFile | None, File()] = None
    sub_image2: Annotated[UploadFile | None, File()] = None
    sub_image3: Annotated[UploadFile | None, File()] = None
    sub_image4: Annotated[UploadFile | None, File()] = None


class SpiritsDict(TypedDict):
    name: str
    # brand ?
    aroma: list[str]
    taste: list[str]
    finish: list[str]
    kind: str
    sub_kind: str
    amount: float  # volume
    alcohol: float  # abv
    origin_nation: str
    origin_location: str
    description: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


class SpiritsSearch(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_camel)

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
    sub_kind: Annotated[
        str | None, Field(min_length=1, description="주류의 세부 종류, 정확한 일치")
    ] = None
    min_alcohol: Annotated[
        float | None, Field(ge=0, description="주류의 최소 알코올 도수")
    ] = None
    max_alcohol: Annotated[
        float | None, Field(ge=0, description="주류의 최대 알코올 도수")
    ] = None
    origin_nation: Annotated[
        str | None, Field(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    origin_location: Annotated[
        str | None, Field(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    page_number: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    page_size: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10

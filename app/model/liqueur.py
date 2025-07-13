from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class LiqueurDict(TypedDict):
    name: str
    brand: str
    taste: list[str]
    kind: str
    sub_kind: str
    main_ingredients: list[str]
    volume: float
    abv: float
    origin_nation: str
    description: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


class LiqueurSearch(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_camel)

    name: Annotated[
        str | None, Field(min_length=1, description="리큐르의 이름, 부분 일치")
    ] = None
    brand: Annotated[
        str | None, Field(min_length=1, description="리큐르의 브랜드, 정확한 일치")
    ] = None
    taste: Annotated[
        list[str] | None,
        Field(min_length=1, description="리큐르의 맛, 목록 중 정확한 일치"),
    ] = None
    kind: Annotated[
        str | None, Field(min_length=1, description="리큐르의 종류, 정확한 일치")
    ] = None
    sub_kind: Annotated[
        str | None, Field(min_length=1, description="리큐르의 세부 종류, 정확한 일치")
    ] = None
    main_ingredients: Annotated[
        list[str] | None,
        Field(min_length=1, description="리큐르의 주재료, 목록 중 정확한 일치"),
    ] = None
    min_volume: Annotated[
        float | None, Field(ge=0, description="리큐르의 최소 용량")
    ] = None
    max_volume: Annotated[
        float | None, Field(ge=0, description="리큐르의 최대 용량")
    ] = None
    min_abv: Annotated[
        float | None, Field(ge=0, description="리큐르의 최소 알코올 도수")
    ] = None
    max_abv: Annotated[
        float | None, Field(ge=0, description="리큐르의 최대 알코올 도수")
    ] = None
    origin_nation: Annotated[
        str | None, Field(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    origin_location: Annotated[
        str | None, Field(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    description: Annotated[
        str | None, Field(min_length=1, description="리큐르의 설명, 부분 일치")
    ] = None
    page_number: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    page_size: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10

from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, Field


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
    model_config = {"extra": "forbid"}

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
    subKind: Annotated[
        str | None, Field(min_length=1, description="리큐르의 세부 종류, 정확한 일치")
    ] = None
    mainIngredients: Annotated[
        list[str] | None,
        Field(min_length=1, description="리큐르의 주재료, 목록 중 정확한 일치"),
    ] = None
    minVolume: Annotated[
        float | None, Field(ge=0, description="리큐르의 최소 용량")
    ] = None
    maxVolume: Annotated[
        float | None, Field(ge=0, description="리큐르의 최대 용량")
    ] = None
    minAbv: Annotated[
        float | None, Field(ge=0, description="리큐르의 최소 알코올 도수")
    ] = None
    maxAbv: Annotated[
        float | None, Field(ge=0, description="리큐르의 최대 알코올 도수")
    ] = None
    originNation: Annotated[
        str | None, Field(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    originLocation: Annotated[
        str | None, Field(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    description: Annotated[
        str | None, Field(min_length=1, description="리큐르의 설명, 부분 일치")
    ] = None
    pageNumber: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    pageSize: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10

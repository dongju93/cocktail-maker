from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from pydantic import BaseModel, Field


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
    minAlcohol: Annotated[
        float | None, Field(ge=0, description="주류의 최소 알코올 도수")
    ] = None
    maxAlcohol: Annotated[
        float | None, Field(ge=0, description="주류의 최대 알코올 도수")
    ] = None
    originNation: Annotated[
        str | None, Field(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    originLocation: Annotated[
        str | None, Field(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    pageNumber: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    pageSize: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10

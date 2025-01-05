from typing import Annotated

from pydantic import BaseModel, Field


class SpiritsRegister(BaseModel):
    model_config = {"extra": "forbid"}

    name: Annotated[str, Field(..., min_length=1)]
    aroma: Annotated[list[str], Field(..., min_length=1)]
    taste: Annotated[list[str], Field(..., min_length=1)]
    finish: Annotated[list[str], Field(..., min_length=1)]
    kind: Annotated[str, Field(...)]
    subKind: Annotated[str, Field(...)]
    amount: Annotated[float, Field(...)]
    alcohol: Annotated[float, Field(...)]
    origin_nation: Annotated[str, Field(...)]
    origin_location: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]


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

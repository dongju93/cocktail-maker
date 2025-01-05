from typing import Annotated, Any

import uvloop
from fastapi import Body, FastAPI, Path, Query
from fastapi.responses import ORJSONResponse

from app.database.query import (
    get_many_spirits_from_mongo,
    get_single_spirits_from_mongo,
    insert_spirits_to_mongo,
)
from app.model.spirits import SpiritsRegister, SpiritsSearch

uvloop.install()

app = FastAPI(
    title="Cocktail maker REST API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)


@app.post(
    "/spirits",
    summary="주류 정보 등록",
    description="""
    <h3>[ 본문 필드 설명 ]</h3>\n
    - name: 이름
    - aroma: 향
    - taste: 맛
    - finish: 끝맛
    - kind: 종류
    - subKind: 세부 종류
    - amount: 용량
    - alcohol: 도수
    - origin_nation: 원산지 국가
    - origin_location: 원산지 지역
    - description: 설명
    """,
)
async def spirits_register(
    items: Annotated[list[SpiritsRegister], Body(...)]
) -> ORJSONResponse:
    inserted_object_id: str = await insert_spirits_to_mongo(items)
    return ORJSONResponse(content={"spirits_oid": inserted_object_id}, status_code=201)


@app.get("/spirits/{name}", summary="단일 주류 정보 조회")
async def spirits_detail(
    name: Annotated[str, Path(..., description="주류의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await get_single_spirits_from_mongo(name)
    return ORJSONResponse(content=spirits, status_code=200)


@app.get("/spirits", summary="주류 정보 검색")
async def spirits_search(
    params: Annotated[SpiritsSearch, Query(...)]
) -> ORJSONResponse:
    data: list[dict[str, Any]] = await get_many_spirits_from_mongo(params)
    return ORJSONResponse(content=data, status_code=200)

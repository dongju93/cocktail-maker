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
    - spirits_id: The unique identifier for a spirits
    - aroma: Aroma of the spirits
    - taste: Taste of the spirits
    - finish: Finish of the spirits
    - kind: Kind of the spirits
    - subKind: Sub-kind of the spirits
    - amount: Amount of the spirits
    - alcohol: Alcohol by volume of the spirits
    - origin_nation: Origin of the spirits
    - origin_location: Location of the spirits
    - description: Description of the spirits
    """,
)
async def register_spirits(item: Annotated[Spirits, Body(...)]) -> ORJSONResponse:
    inserted_object_id: str = await insert_spirits_to_mongo(item)
    return ORJSONResponse(content={"spirits_oid": inserted_object_id}, status_code=201)


@app.get("/spirits/{spirits_id}")
async def get_spirits(spirits_id: Annotated[int, Path(...)]) -> ORJSONResponse:
    spirits: dict[str, Any] = await get_spirits_from_mongo(spirits_id)
    return ORJSONResponse(content=spirits, status_code=200)


@app.get("/spirits")
async def spirits_search(
    params: Annotated[SpiritsSearch, Query(...)]
) -> ORJSONResponse:
    data: list[dict[str, Any]] = await get_many_spirits_from_mongo(params)
    return ORJSONResponse(content=data, status_code=200)

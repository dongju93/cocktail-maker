from typing import Annotated, Any

import uvloop
from fastapi import Body, FastAPI, Query
from fastapi.responses import ORJSONResponse

from app.database.query import get_spirits_from_mongo, insert_spirits_to_mongo
from app.model.spirits import Spirits

uvloop.install()

app = FastAPI(
    title="Cocktail maker REST API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)


@app.post("/spirits")
async def register_spirits(item: Annotated[Spirits, Body(...)]) -> ORJSONResponse:
    inserted_object_id: str = await insert_spirits_to_mongo(item)
    return ORJSONResponse(content={"spirits_oid": inserted_object_id}, status_code=201)


@app.get("/spirits")
async def get_spirits(spirits_id: Annotated[int, Query(...)]) -> ORJSONResponse:
    spirits: dict[str, Any] = await get_spirits_from_mongo(spirits_id)
    return ORJSONResponse(content=spirits, status_code=200)

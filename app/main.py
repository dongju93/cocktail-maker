import uvloop
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.model.spirits import Spirits

uvloop.install()

app = FastAPI(
    title="Cocktail maker REST API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)


@app.post("spirits")
async def register_spirits(item: Spirits):
    return "success"


@app.get("spirits")
async def get_spirits():
    return "success"

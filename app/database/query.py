from typing import Any

from fastapi import HTTPException
from pymongo.results import InsertOneResult

from app.database.connector import mongodb_conn
from app.model.spirits import Spirits


async def insert_spirits_to_mongo(item: Spirits) -> str:
    try:
        data: dict[str, Any] = item.model_dump()
        async with mongodb_conn("spirits") as conn:
            result: InsertOneResult = await conn.insert_one(data)
    except Exception as e:
        print("Insert Spirits object to mongodb raise an error")
        raise e

    return str(result.inserted_id)


async def get_spirits_from_mongo(spirits_id: int) -> dict[str, Any]:
    try:
        async with mongodb_conn("spirits") as conn:
            result: dict[str, Any] | None = await conn.find_one(
                {"spirits_id": spirits_id}
            )
            if result is None:
                raise HTTPException(status_code=404, detail="Spirits not found")
    except Exception as e:
        print("Get Spirits object from mongodb raise an error")
        raise e
    else:
        result["_id"] = str(result["_id"])

    return result

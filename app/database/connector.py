import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator  # noqa: UP035

from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

load_dotenv(dotenv_path=".env")
MONGODB_URL: str = os.environ["mongodb_url"]


@asynccontextmanager
async def mongodb_conn(collection: str) -> AsyncGenerator[AsyncIOMotorCollection, None]:
    uri: str = MONGODB_URL
    conn: AsyncIOMotorClient = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    db: AsyncIOMotorDatabase = conn["cocktail-db"]
    try:
        yield db[collection]
    finally:
        conn.close()

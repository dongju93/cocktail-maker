import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator  # noqa: UP035

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(dotenv_path="app/.env")
MONGODB_URL: str | None = os.getenv("mongodb_url")


@asynccontextmanager
async def mongodb_conn() -> AsyncGenerator[AsyncIOMotorClient, None]:
    if MONGODB_URL is None:
        raise ValueError("MONGODB_URL is not set")
    uri: str = MONGODB_URL
    conn: AsyncIOMotorClient = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    try:
        yield conn
    finally:
        conn.close()

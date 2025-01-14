import os
from contextlib import asynccontextmanager, contextmanager
from sqlite3 import Connection
from typing import AsyncGenerator, Generator  # noqa: UP035

from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

load_dotenv(dotenv_path=".env")
MONGODB_URL: str = os.environ["MONGODB_URL"]
SQLITE_PATH: str = os.environ["SQLITE_PATH"]


@asynccontextmanager
async def mongodb_conn(collection: str) -> AsyncGenerator[AsyncIOMotorCollection, None]:
    conn: AsyncIOMotorClient = AsyncIOMotorClient(
        MONGODB_URL, serverSelectionTimeoutMS=5000
    )
    db: AsyncIOMotorDatabase = conn["cocktail-db"]
    try:
        yield db[collection]
    finally:
        conn.close()


@contextmanager
def sqlite_conn() -> Generator[Connection, None, None]:
    conn = Connection(
        database=SQLITE_PATH,
        timeout=10,
        cached_statements=100,
        check_same_thread=True,
        isolation_level=None,
        autocommit=False,
    )
    try:
        yield conn
    finally:
        conn.close()

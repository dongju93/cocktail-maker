import os
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator  # noqa: UP035

from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from sqlmodel import Session

from database.table import engine

load_dotenv(dotenv_path=".env")
MONGODB_URL: str = os.environ["MONGODB_URL"]
SQLITE_PATH: str = os.environ["SQLITE_PATH"]


@asynccontextmanager
async def mongodb_conn(collection: str) -> AsyncGenerator[AsyncIOMotorCollection]:
    conn: AsyncIOMotorClient = AsyncIOMotorClient(
        MONGODB_URL, serverSelectionTimeoutMS=5000
    )
    db: AsyncIOMotorDatabase = conn["cocktail-db"]
    try:
        yield db[collection]
    finally:
        conn.close()


@contextmanager
def sqlite_conn_orm() -> Generator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

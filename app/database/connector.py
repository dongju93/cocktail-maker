from contextlib import asynccontextmanager, contextmanager
from os import environ
from typing import AsyncGenerator, Generator  # noqa: UP035

from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from sqlmodel import Session

from .table import engine

load_dotenv()
MONGODB_URL: str = environ["MONGODB_URL"]
SQLITE_PATH: str = environ["SQLITE_PATH"]


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

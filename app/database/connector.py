from contextlib import asynccontextmanager, contextmanager
from os import environ
from typing import AsyncGenerator, Generator  # noqa: UP035

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from sqlmodel import Session

from .table import engine

load_dotenv()
MONGODB_URL: str = environ["MONGODB_URL"]
SQLITE_PATH: str = environ["SQLITE_PATH"]


@asynccontextmanager
async def mongodb_conn(collection: str) -> AsyncGenerator[AsyncCollection]:
    conn: AsyncMongoClient = AsyncMongoClient(
        MONGODB_URL, serverSelectionTimeoutMS=5000
    )
    db: AsyncDatabase = conn["cocktail-db"]
    try:
        yield db[collection]
    finally:
        await conn.close()


@contextmanager
def sqlite_conn_orm() -> Generator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

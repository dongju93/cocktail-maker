from os import environ

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import Field, SQLModel, create_engine

load_dotenv()
SQLITE_PATH: str = environ["SQLITE_PATH"]


class MetadataTable(SQLModel, table=True):
    __tablename__ = "metadata"  # type: ignore

    id: int = Field(primary_key=True)
    category: str
    name: str
    kind: str


engine: Engine = create_engine(f"sqlite:///{SQLITE_PATH}")
SQLModel.metadata.create_all(engine)

from sqlmodel import Field, SQLModel


class SpritsMetadata(SQLModel, table=True):
    __tablename__ = "spirits_metadata"

    id: int = Field(primary_key=True)
    category: str
    name: str = Field(unique=True)

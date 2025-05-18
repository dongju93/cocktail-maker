from datetime import datetime
from typing import NotRequired, TypedDict


class IngredientDict(TypedDict):
    name: str
    brand: list[str] | None
    kind: str
    description: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]

from datetime import datetime
from typing import NotRequired, TypedDict


class LiqueurDict(TypedDict):
    name: str
    brand: str
    taste: list[str]
    kind: str
    sub_kind: str
    main_ingredients: list[str]
    volume: float
    abv: float
    origin_nation: str
    description: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]

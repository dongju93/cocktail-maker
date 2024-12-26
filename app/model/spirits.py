from typing import Annotated

from pydantic import BaseModel, Field


class Spirits(BaseModel):
    model_config = {"extra": "forbid"}

    spirits_id: Annotated[int, Field(...)]
    aroma: Annotated[list[str], Field(..., min_length=1)]
    taste: Annotated[list[str], Field(..., min_length=1)]
    finish: Annotated[list[str], Field(..., min_length=1)]
    kind: Annotated[str, Field(...)]
    subKind: Annotated[str, Field(...)]
    amount: Annotated[float, Field(...)]
    alcohol: Annotated[float, Field(...)]
    origin_nation: Annotated[str, Field(...)]
    origin_location: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]

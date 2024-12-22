from pydantic import BaseModel, Field


class Spirits(BaseModel):
    model_config = {"extra": "forbid"}

    spirits_id: int = Field(..., description="The unique identifier for a spirits")
    aroma: list[str] = Field(..., description="Aroma of the spirits", min_length=1)
    taste: list[str] = Field(..., description="Taste of the spirits", min_length=1)
    finish: list[str] = Field(..., description="Finish of the spirits", min_length=1)
    kind: str = Field(..., description="Kind of the spirits")
    amount: float = Field(..., description="Amount of the spirits")
    alcohol: float = Field(..., description="Alcohol by volume of the spirits")
    origin_nation: str = Field(..., description="Origin of the spirits")
    origin_location: str = Field(..., description="Location of the spirits")
    description: str = Field(..., description="Description of the spirits")

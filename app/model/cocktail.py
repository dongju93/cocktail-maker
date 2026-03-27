from datetime import datetime
from enum import StrEnum
from typing import Annotated, NotRequired, TypedDict

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class IngredientType(StrEnum):
    SPIRITS = "spirits"
    LIQUEUR = "liqueur"
    INGREDIENT = "ingredient"


class Recipe(BaseModel):
    """칵테일 제조 레시피, 이미 등록된 정보를 참조"""

    id: Annotated[str, Field()]
    type: Annotated[str, Field()]
    amount: Annotated[int, Field()]
    unit: Annotated[str, Field()]

    @field_validator("type")
    @classmethod
    def normalize_type(cls, value: str) -> str:
        normalized_type = "liqueur" if value == "liquor" else value
        allowed_types = {item.value for item in IngredientType}

        if normalized_type not in allowed_types:
            raise ValueError(f"type must be one of {', '.join(sorted(allowed_types))}")

        return normalized_type


class RecipeStep(BaseModel):
    """칵테일 제조 순서 및 설명"""

    step: Annotated[int, Field(ge=1)]
    description: Annotated[str, Field()]


class CocktailData(BaseModel):
    name: Annotated[str, Field()]
    aroma: Annotated[list[str], Field(min_length=1)]
    taste: Annotated[list[str], Field(min_length=1)]
    finish: Annotated[list[str], Field(min_length=1)]
    ingredients: Annotated[list[Recipe], Field()]
    steps: Annotated[list[RecipeStep], Field()]
    glass: Annotated[str, Field()]
    description: Annotated[str, Field()]
    origin_nation: Annotated[str, Field()]


class CocktailRegisterData(CocktailData):
    pass


class CocktailUpdateData(CocktailData):
    pass


class CocktailSearchQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[
        str | None, Query(min_length=1, description="칵테일 이름, 부분 일치")
    ] = None
    aroma: Annotated[
        list[str] | None,
        Query(min_length=1, description="칵테일 향, 목록 중 정확한 일치"),
    ] = None
    taste: Annotated[
        list[str] | None,
        Query(min_length=1, description="칵테일 맛, 목록 중 정확한 일치"),
    ] = None
    finish: Annotated[
        list[str] | None,
        Query(min_length=1, description="칵테일 여운, 목록 중 정확한 일치"),
    ] = None
    glass: Annotated[
        str | None, Query(min_length=1, description="칵테일 잔 종류, 정확한 일치")
    ] = None
    origin_nation: Annotated[
        str | None, Query(min_length=1, description="칵테일 기원 국가, 정확한 일치")
    ] = None
    description: Annotated[
        str | None, Query(min_length=1, description="칵테일 설명, 부분 일치")
    ] = None
    ingredient_ids: Annotated[
        list[str] | None,
        Query(min_length=1, description="레시피에 포함된 재료 문서 ID 목록"),
    ] = None
    page_number: Annotated[int, Query(..., ge=1, description="페이지 번호")] = 1
    page_size: Annotated[int, Query(..., ge=1, le=100, description="페이지 크기")] = 10


class RecipeDict(TypedDict):
    id: str
    type: str
    amount: int
    unit: str


class RecipeStepDict(TypedDict):
    step: int
    description: str


class CocktailDict(TypedDict):
    name: str
    aroma: list[str]
    taste: list[str]
    finish: list[str]
    ingredients: list[RecipeDict]
    steps: list[RecipeStepDict]
    glass: str
    description: str
    origin_nation: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]

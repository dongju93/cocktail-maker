from datetime import datetime
from enum import Enum
from typing import Annotated, NotRequired, TypedDict

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class IngredientType(str, Enum):
    SPIRITS = "spirits"
    LIQUOR = "liquor"
    INGREDIENT = "ingredient"


class Recipe(BaseModel):
    """칵테일 제조 레시피, 이미 등록된 정보를 참조"""

    id: Annotated[str, Field()]
    type: Annotated[str, Field()]
    amount: Annotated[int, Field()]
    unit: Annotated[str, Field()]


class RecipeStep(BaseModel):
    """칵테일 제조 순서 및 설명"""

    step: Annotated[int, Field(ge=1)]
    description: Annotated[str, Field()]


class CocktailForm(BaseModel):
    name: Annotated[str, Field()]
    aroma: Annotated[list[str], Field(min_length=1)]
    taste: Annotated[list[str], Field(min_length=1)]
    finish: Annotated[list[str], Field(min_length=1)]
    ingredients: Annotated[list[Recipe], Field()]
    steps: Annotated[list[RecipeStep], Field()]
    glass: Annotated[str, Field()]
    description: Annotated[str, Field()]
    origin_nation: Annotated[str, Field()]
    main_image: Annotated[
        UploadFile,
        File(
            description="칵테일의 대표 이미지, 최대 2MB",
            media_type=[  # type: ignore
                "image/jpeg",
                "image/png",
                "image/jpg",
                "image/webp",
                "image/bmp",
                "image/gif",
                "image/tiff",
            ],
        ),
    ]
    sub_image1: Annotated[UploadFile | None, File()] = None
    sub_image2: Annotated[UploadFile | None, File()] = None
    sub_image3: Annotated[UploadFile | None, File()] = None
    sub_image4: Annotated[UploadFile | None, File()] = None


class CocktailRegisterForm(CocktailForm):
    pass


class CocktailUpdateForm(CocktailForm):
    pass


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

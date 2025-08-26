from enum import Enum
from typing import Annotated

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class IngredientType(str, Enum):
    SPIRITS = "spirits"
    LIQUOR = "liquor"
    INGREDIENT = "ingredient"


class Recipe(BaseModel):
    id: Annotated[str, Field()]
    type: Annotated[str, Field()]
    amount: Annotated[int, Field()]
    unit: Annotated[str, Field()]


class RecipeStep(BaseModel):
    step: Annotated[int, Field(ge=1)]
    description: Annotated[str, Field()]


class CocktailRegister(BaseModel):
    name: Annotated[str, Field()]
    ingredients: Annotated[list[Recipe], Field()]
    steps: Annotated[list[RecipeStep], Field()]
    glass: Annotated[str, Field()]
    tags: Annotated[list[str], Field()]
    description: Annotated[str, Field()]
    origin_nation: Annotated[str, Field()]
    main_image: Annotated[
        UploadFile,
        File(
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

from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .validation import HangulValidationMixIn


class IngredientDict(TypedDict):
    name: str
    brand: list[str] | None
    kind: str
    description: str
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


class IngredientSearch(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=to_camel)

    name: Annotated[
        str | None, Field(min_length=1, description="재료의 이름, 부분 일치")
    ] = None
    brand: Annotated[
        list[str] | None,
        Field(min_length=1, description="재료의 브랜드, 목록 중 정확한 일치"),
    ] = None
    kind: Annotated[
        str | None, Field(min_length=1, description="재료의 종류, 정확한 일치")
    ] = None
    description: Annotated[
        str | None, Field(min_length=1, description="재료의 설명, 부분 일치")
    ] = None
    page_number: Annotated[int, Field(..., ge=1, description="페이지 번호")] = 1
    page_size: Annotated[int, Field(..., ge=1, le=100, description="페이지 크기")] = 10


class IngredientForm(BaseModel, HangulValidationMixIn):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="재료의 이름",
        ),
    ]
    kind: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            description="재료의 종류",
        ),
    ]
    description: Annotated[
        str,
        Field(
            min_length=1,
            max_length=1000,
            description="재료의 설명",
        ),
    ]
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
            description="대표 이미지, 최대 2MB",
        ),
    ]
    brand: Annotated[
        list[str] | None,
        Field(
            min_length=1,
            max_length=10,
            description="브랜드",
        ),
    ] = None


class IngredientRegisterForm(IngredientForm): ...


class IngredientUpdateForm(IngredientForm): ...

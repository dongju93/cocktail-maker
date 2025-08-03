from datetime import datetime
from typing import Annotated, NotRequired, TypedDict

from fastapi import File, Query, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


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


class LiqueurSearchQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[
        str | None, Query(min_length=1, description="리큐르의 이름, 부분 일치")
    ] = None
    brand: Annotated[
        str | None, Query(min_length=1, description="리큐르의 브랜드, 정확한 일치")
    ] = None
    taste: Annotated[
        list[str] | None,
        Query(min_length=1, description="리큐르의 맛, 목록 중 정확한 일치"),
    ] = None
    kind: Annotated[
        str | None, Query(min_length=1, description="리큐르의 종류, 정확한 일치")
    ] = None
    sub_kind: Annotated[
        str | None, Query(min_length=1, description="리큐르의 세부 종류, 정확한 일치")
    ] = None
    main_ingredients: Annotated[
        list[str] | None,
        Query(min_length=1, description="리큐르의 주재료, 목록 중 정확한 일치"),
    ] = None
    min_volume: Annotated[
        float | None, Query(ge=0, description="리큐르의 최소 용량")
    ] = None
    max_volume: Annotated[
        float | None, Query(ge=0, description="리큐르의 최대 용량")
    ] = None
    min_abv: Annotated[
        float | None, Query(ge=0, description="리큐르의 최소 알코올 도수")
    ] = None
    max_abv: Annotated[
        float | None, Query(ge=0, description="리큐르의 최대 알코올 도수")
    ] = None
    origin_nation: Annotated[
        str | None, Query(min_length=1, description="원산지 국가, 정확한 일치")
    ] = None
    origin_location: Annotated[
        str | None, Query(min_length=1, description="원산지 지역, 부분 일치")
    ] = None
    description: Annotated[
        str | None, Query(min_length=1, description="리큐르의 설명, 부분 일치")
    ] = None
    page_number: Annotated[int, Query(..., ge=1, description="페이지 번호")] = 1
    page_size: Annotated[int, Query(..., ge=1, le=100, description="페이지 크기")] = 10


class LiqueurRegisterForm(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 이름",
        ),
    ]
    brand: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 브랜드",
        ),
    ]
    taste: Annotated[
        list[str],
        Field(
            min_length=1,
            max_length=10,
            description="리큐르의 맛",
        ),
    ]
    kind: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 종류",
        ),
    ]
    sub_kind: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 세부 종류",
        ),
    ]
    main_ingredients: Annotated[
        list[str],
        Field(
            min_length=1,
            description="리큐르의 주재료",
        ),
    ]
    volume: Annotated[
        float,
        Field(
            ge=0,
            le=1000,
            decimal_places=2,
            description="리큐르의 용량(mL)",
        ),
    ]
    abv: Annotated[
        float,
        Field(
            ge=0,
            le=100,
            decimal_places=2,
            description="리큐르의 알코올 도수",
        ),
    ]
    origin_nation: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 원산지 국가",
        ),
    ]
    description: Annotated[
        str,
        Field(
            min_length=1,
            max_length=1000,
            description="리큐르의 설명",
        ),
    ]
    main_image: Annotated[
        UploadFile,
        File(
            ...,
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


class LiqueurUpdateForm(LiqueurRegisterForm):
    model_config = ConfigDict(alias_generator=to_camel)

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 이름",
        ),
    ]
    brand: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 브랜드",
        ),
    ]
    taste: Annotated[
        list[str],
        Field(
            min_length=1,
            max_length=10,
            description="리큐르의 맛",
        ),
    ]
    kind: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 종류",
        ),
    ]
    sub_kind: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 세부 종류",
        ),
    ]
    main_ingredients: Annotated[
        list[str],
        Field(
            min_length=1,
            description="리큐르의 주재료",
        ),
    ]
    volume: Annotated[
        float,
        Field(
            ge=0,
            le=1000,
            decimal_places=2,
            description="리큐르의 용량(mL)",
        ),
    ]
    abv: Annotated[
        float,
        Field(
            ge=0,
            le=100,
            decimal_places=2,
            description="리큐르의 알코올 도수",
        ),
    ]
    origin_nation: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="리큐르의 원산지 국가",
        ),
    ]
    description: Annotated[
        str,
        Field(
            min_length=1,
            max_length=1000,
            description="리큐르의 설명",
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
            description="대표 이미지, 최대 2MB (선택 사항)",
        ),
    ]

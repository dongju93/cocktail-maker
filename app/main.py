from datetime import UTC, datetime
from typing import Annotated, Any

import uvloop
from fastapi import (
    Body,
    FastAPI,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    Security,
    UploadFile,
)
from fastapi.responses import ORJSONResponse

from auth import refresh_access_token, sign_in_token, verify_token
from database.query import (
    get_many_spirits_from_mongo,
    get_single_spirits_from_mongo,
    get_spirits_metadata_from_sqlite,
    insert_spirits_metadata_to_sqlite,
    insert_spirits_to_mongo,
    user_sign_in,
    user_sign_up,
)
from model.response import SpiritsSearchResponse
from model.spirits import (
    Category,
    SpiritsMetadataRegister,
    SpiritsRegister,
    SpiritsSearch,
)
from model.user import Login, User
from model.validation import (
    is_image_content_type,
    is_image_size_too_large,
    read_nullable_image,
)

uvloop.install()

app = FastAPI(
    title="Cocktail maker REST API",
    # version: major.minor.patch[-build]
    version="0.1.0-dev",
    summary="칵테일 제조법과 주류 및 재료 정보 제공",
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
    ],
    default_response_class=ORJSONResponse,
)


@app.post("/signUp", summary="회원가입")
async def sign_up(user: Annotated[User, Body(...)]) -> ORJSONResponse:
    """
    회원가입과 동시에 로그인을 수행하므로, 회원가입 성공 시 메시지와 함께 JWT 를 반환
    """
    if not await user_sign_up(user):
        return ORJSONResponse(
            content={"message": "User already exists"}, status_code=409
        )

    login = Login(
        user_id=user.user_id,
        password=user.password,
    )
    if (roles := await user_sign_in(login)) == []:
        return ORJSONResponse(
            content={"message": "Invalid user_id or password"}, status_code=401
        )
    jwt: dict[str, str] = sign_in_token(login.user_id, roles)
    return ORJSONResponse(
        content={"message": "User successfully created", "tokens": jwt}, status_code=201
    )


@app.post("/signIn", summary="로그인")
async def sign_in(login: Annotated[Login, Body(...)]) -> ORJSONResponse:
    """
    로그인 성공 시 메시지와 함께 JWT 를 반환
    """
    if (roles := await user_sign_in(login)) == []:
        return ORJSONResponse(
            content={"message": "Invalid user_id or password"}, status_code=401
        )
    jwt: dict[str, str] = sign_in_token(login.user_id, roles)
    return ORJSONResponse(
        content={"message": "Successfully login", "tokens": jwt}, status_code=200
    )


@app.post("/refreshToken", summary="액세스 토큰 갱신")
async def refresh_token(request: Request) -> ORJSONResponse:
    """
    리프레시 토큰을 Header에서 받아 액세스 토큰을 갱신
    """
    auth_header: str | None = request.headers.get("Authorization")
    if auth_header is None:
        return ORJSONResponse(
            content={"message": "Refresh token is required"}, status_code=401
        )
    if not auth_header.startswith("Bearer "):
        return ORJSONResponse(
            content={"message": "Invalid authorization header format"}, status_code=401
        )

    # 실제 Bearer 토큰 부분을 분리
    refresh_token: str = auth_header.split(" ")[1]

    refreshed_access_token: dict[str, str] = await refresh_access_token(refresh_token)
    return ORJSONResponse(
        content={
            "message": "Successfully refresh token",
            "token": refreshed_access_token,
        },
        status_code=200,
    )


@app.post(
    "/spirits",
    summary="주류 정보 등록",
    description="""
    <h3>[ 본문 필드 설명 ]</h3>\n
    - name: 이름
    - aroma: 향
    - taste: 맛
    - finish: 끝맛
    - kind: 종류
    - subKind: 세부 종류
    - amount: 용량
    - alcohol: 도수
    - origin_nation: 원산지 국가
    - origin_location: 원산지 지역
    - description: 설명
    """,
)
async def spirits_register(  # noqa
    name: Annotated[str, Form(..., min_length=1)],
    aroma: Annotated[list[str], Form(..., min_length=1)],
    taste: Annotated[list[str], Form(..., min_length=1)],
    finish: Annotated[list[str], Form(..., min_length=1)],
    kind: Annotated[str, Form(...)],
    subKind: Annotated[str, Form(...)],
    amount: Annotated[float, Form(...)],
    alcohol: Annotated[float, Form(...)],
    origin_nation: Annotated[str, Form(...)],
    origin_location: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    mainImage: Annotated[
        UploadFile,
        File(..., description="주류의 대표 이미지, 최대 2MB"),
    ],
    subImage1: Annotated[UploadFile | None, File()] = None,
    subImage2: Annotated[UploadFile | None, File()] = None,
    subImage3: Annotated[UploadFile | None, File()] = None,
    subImage4: Annotated[UploadFile | None, File()] = None,
) -> ORJSONResponse:
    try:
        # 이미지 파일 타입 검사
        for image in [mainImage, subImage1, subImage2, subImage3, subImage4]:
            if not await is_image_content_type(image):
                raise HTTPException(422, "Invalid file extension")

        # 이미지 파일 앍가
        read_main_image: bytes = await mainImage.read()
        read_sub_image1: bytes | None = await read_nullable_image(subImage1)
        read_sub_image2: bytes | None = await read_nullable_image(subImage2)
        read_sub_image3: bytes | None = await read_nullable_image(subImage3)
        read_sub_image4: bytes | None = await read_nullable_image(subImage4)

        # 이미지 파일 크기 검사
        for image_byte in [
            read_main_image,
            read_sub_image1,
            read_sub_image2,
            read_sub_image3,
            read_sub_image4,
        ]:
            if not await is_image_size_too_large(image_byte):
                raise HTTPException(422, "File size is too large, maximum 2MB")

        item: SpiritsRegister = SpiritsRegister(
            name=name,
            aroma=aroma,
            taste=taste,
            finish=finish,
            kind=kind,
            subKind=subKind,
            amount=amount,
            alcohol=alcohol,
            origin_nation=origin_nation,
            origin_location=origin_location,
            description=description,
            main_image=read_main_image,
            sub_image1=read_sub_image1,
            sub_image2=read_sub_image2,
            sub_image3=read_sub_image3,
            sub_image4=read_sub_image4,
            created_at=datetime.now(tz=UTC),
        )
        data: str = await insert_spirits_to_mongo(item)
        code: int = 201
    except HTTPException as he:
        data = he.detail
        code = he.status_code
    except Exception as e:
        data = f"{e!s}"
        code = 500

    return ORJSONResponse(content={"data": data}, status_code=code)


@app.get("/spirits/{name}", summary="단일 주류 정보 조회")
async def spirits_detail(
    name: Annotated[str, Path(..., description="주류의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await get_single_spirits_from_mongo(name)
    return ORJSONResponse(content=spirits, status_code=200)


@app.get("/spirits", summary="주류 정보 검색")
async def spirits_search(
    params: Annotated[SpiritsSearch, Query(...)],
    _: Annotated[None, Security(verify_token(["admin", "user"]))],
) -> ORJSONResponse:
    data: SpiritsSearchResponse = await get_many_spirits_from_mongo(params)
    return ORJSONResponse(content=data, status_code=200)


@app.post("/spirits/metadata", summary="주류 정보 메타데이터 등록")
async def spirits_metadata_register(
    items: Annotated[SpiritsMetadataRegister, Body(...)],
) -> ORJSONResponse:
    try:
        if not insert_spirits_metadata_to_sqlite(items):
            messages = "Metadata registration failed"
            status_code = 409
        else:
            messages = "Metadata registration successful"
            status_code = 201
    except Exception as e:
        messages = f"Metadata registration failed: {e!s}"
        status_code = 500

    return ORJSONResponse(content={"message": messages}, status_code=status_code)


@app.get("/spirits/metadata/{category}", summary="주류 정보 메타데이터 조회")
async def spirits_metadata_details(
    category: Annotated[Category, Path(..., description="메타데이터 카테고리")],
) -> ORJSONResponse:
    metadata: list[str] = get_spirits_metadata_from_sqlite(category)
    return ORJSONResponse(content=metadata, status_code=200)


@app.delete("/spirits/metadata/{id}", summary="주류 정보 메타데이터 삭제")
async def spirits_metadata_remover(
    id: Annotated[int, Path(..., description="메타데이터 인덱스")],
) -> ORJSONResponse:
    # metadata: list[str] = get_spirits_metadata_from_sqlite(category)
    return ORJSONResponse(content=None, status_code=200)


@app.get("/version", summary="서비스 버전 확인")
async def version() -> ORJSONResponse:
    return ORJSONResponse(content={"version": version}, status_code=200)

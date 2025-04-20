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
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi.responses import ORJSONResponse
from structlog import BoundLogger

from auth import refresh_access_token, sign_in_token, verify_token
from database.query import (
    CreateSpirits,
    CreateSpiritsMetadata,
    DeleteSpirits,
    DeleteSpiritsMetadata,
    ReadSpirits,
    ReadSpiritsMetadata,
    UpdateSpirits,
    Users,
)
from model.etc import ResponseFormat
from model.response import SpiritsSearchResponse
from model.spirits import (
    SpiritsDict,
    SpiritsMetadataCategory,
    SpiritsMetadataRegister,
    SpiritsSearch,
)
from model.user import Login, User
from model.validation import (
    ImageValidation,
    MetadataValidation,
)
from utils.etc import return_formatter
from utils.logger import Logger

uvloop.install()

logger: BoundLogger = Logger().setup()

app = FastAPI(
    title="Cocktail maker REST API",
    # semantic-versioning: major.minor.patch[-build]
    version="0.1.0-dev",
    summary="칵테일 제조법과 주류 및 재료 정보 제공",
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
    ],
    default_response_class=ORJSONResponse,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


@app.post("/signup", summary="회원가입", tags=["인증"])
async def sign_up(user: Annotated[User, Body(...)]) -> Response:
    """
    회원가입과 동시에 로그인을 수행하므로, 회원가입 성공 시 메시지와 함께 JWT 를 반환
    """
    try:
        if not await Users.sign_up(user):
            raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

        login = Login(
            user_id=user.user_id,
            password=user.password,
        )
        if (roles := await Users.sign_in(login)) == []:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid user_id or password"
            )

        jwt: dict[str, str] = sign_in_token(login.user_id, roles)

    except HTTPException as he:
        return Response(
            await return_formatter("failed", he.status_code, None, he.detail),
            he.status_code,
        )

    response = Response(status_code=204)

    response.set_cookie(
        key="accessToken",
        value=jwt["accessToken"],
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 15분 (초 단위)
        path="/",
        secure=True,  # HTTPS에서만 전송
        samesite="lax",  # CSRF 방지
    )
    response.set_cookie(
        key="refreshToken",
        value=jwt["refreshToken"],
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 7일 (초 단위)
        path="/refresh-token",  # 사용 가능 엔드포인트 제한
        secure=True,
        samesite="strict",
    )

    return response


@app.post("/signin", summary="로그인", tags=["인증"])
async def sign_in(login: Annotated[Login, Body(...)]) -> Response:
    """
    로그인 성공 시 메시지와 함께 JWT 를 반환
    """
    try:
        if (roles := await Users.sign_in(login)) == []:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid user_id or password"
            )

        jwt: dict[str, str] = sign_in_token(login.user_id, roles)

        logger.info("User successfully logged in", user_id=login.user_id, roles=roles)

    except HTTPException as he:
        return Response(
            await return_formatter("failed", he.status_code, None, he.detail),
            he.status_code,
        )

    response = Response(status_code=204)

    response.set_cookie(
        key="accessToken",
        value=jwt["accessToken"],
        httponly=True,  # JavaScript 접근 불가
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refreshToken",
        value=jwt["refreshToken"],
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/refresh-token",
        secure=True,
        samesite="lax",
    )

    return response


@app.post("/refresh-token", summary="액세스 토큰 갱신", tags=["인증"])
async def refresh_token(request: Request) -> Response:
    """
    리프레시 토큰을 Header에서 받아 액세스 토큰을 갱신
    """
    refresh_token: str | None = request.cookies.get("refreshToken")

    try:
        if refresh_token is None:
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        # 액세스 토큰 갱신
        new_token: dict[str, str] = await refresh_access_token(refresh_token)

        logger.info(
            "Access token successfully refreshed", used_token=new_token["accessToken"]
        )

    except HTTPException as he:
        return Response(
            await return_formatter("failed", he.status_code, None, he.detail),
            he.status_code,
        )

    # 응답 생성
    response = Response(status_code=204)

    # 새 액세스 토큰으로 쿠키 갱신
    response.set_cookie(
        key="accessToken",
        value=new_token["accessToken"],
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        secure=True,
        samesite="lax",
    )

    return response


@app.post(
    "/spirits",
    summary="주류 정보 등록",
    tags=["주류"],
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
    - mainImage: 대표 이미지
    - subImage1~4: 보조 이미지
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
    """
    단일 주류 정보 등록
    """

    try:
        # 이미지 검증 및 변환
        read_main_image, sub_images_bytes = await ImageValidation.files(
            mainImage, [subImage1, subImage2, subImage3, subImage4]
        )
        read_sub_image1, read_sub_image2, read_sub_image3, read_sub_image4 = (
            sub_images_bytes
        )

        # 메타데이터 검증
        listed_aroma, listed_taste, listed_finish = await MetadataValidation.data(
            aroma, taste, finish
        )

        item: SpiritsDict = SpiritsDict(
            name=name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=kind,
            subKind=subKind,
            amount=amount,
            alcohol=alcohol,
            origin_nation=origin_nation,
            origin_location=origin_location,
            description=description,
            created_at=datetime.now(tz=UTC),
        )
        data: str = await CreateSpirits(
            item,
            read_main_image,
            read_sub_image1,
            read_sub_image2,
            read_sub_image3,
            read_sub_image4,
        ).save()

        logger.info("Spirits successfully registered", name=name)

        formatted_response: ResponseFormat = await return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register spirits"
        )

    except HTTPException as he:
        logger.error(
            "Failed to register spirits", code=he.status_code, message=he.detail
        )
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
    except Exception as e:
        logger.error("Failed to register spirits", error=str(e))
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to register spirits: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.put("/spirits/{document_id}", summary="주류 정보 수정", tags=["주류"])
async def spirits_update(  # noqa: PLR0913
    document_id: Annotated[str, Path(..., min_length=1, max_length=255)],
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
    """
    주류 정보 수정
    """
    try:
        # 이미지 검증 및 변환
        read_main_image, sub_images_bytes = await ImageValidation.files(
            mainImage, [subImage1, subImage2, subImage3, subImage4]
        )
        read_sub_image1, read_sub_image2, read_sub_image3, read_sub_image4 = (
            sub_images_bytes
        )

        # 메타데이터 검증
        listed_aroma, listed_taste, listed_finish = await MetadataValidation.data(
            aroma, taste, finish
        )

        item: SpiritsDict = SpiritsDict(
            name=name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=kind,
            subKind=subKind,
            amount=amount,
            alcohol=alcohol,
            origin_nation=origin_nation,
            origin_location=origin_location,
            description=description,
            updated_at=datetime.now(tz=UTC),
        )
        await UpdateSpirits(
            document_id,
            item,
            read_main_image,
            read_sub_image1,
            read_sub_image2,
            read_sub_image3,
            read_sub_image4,
        ).update()

        logger.info("Spirits successfully registered", name=name)

        formatted_response: ResponseFormat = await return_formatter(
            "success", status.HTTP_204_NO_CONTENT, None, "Successfully update spirits"
        )

    except HTTPException as he:
        logger.error("Failed to update spirits", code=he.status_code, message=he.detail)
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
    except Exception as e:
        logger.error("Failed to update spirits", error=str(e))
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to update spirits: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.get("/spirits/{name}", summary="단일 주류 정보 조회", tags=["주류"])
async def spirits_detail(
    name: Annotated[str, Path(..., description="주류의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await ReadSpirits.based_on_name(name)

    formatted_response: ResponseFormat = await return_formatter(
        "success", status.HTTP_200_OK, spirits, "Successfully get spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.get("/spirits", summary="주류 정보 검색", tags=["주류"])
async def spirits_search(
    params: Annotated[SpiritsSearch, Query(...)],
    _: Annotated[None, Security(verify_token(["admin", "user"]))],
) -> ORJSONResponse:
    data: SpiritsSearchResponse = await ReadSpirits.search(params)

    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, data, "Successfully search spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.delete("/spirits/{id}", summary="주류 정보 삭제", tags=["주류"])
async def spirits_remover(
    id: Annotated[str, Path(...)],
) -> ORJSONResponse:
    await DeleteSpirits(id).remove()

    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, None, "Successfully delete spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.post(
    "/spirits/metadata/{category}", summary="주류 정보 메타데이터 등록", tags=["주류"]
)
async def spirits_metadata_register(
    category: Annotated[
        SpiritsMetadataCategory, Path(..., description="메타데이터 카테고리")
    ],
    items: Annotated[SpiritsMetadataRegister, Body(...)],
) -> ORJSONResponse:
    try:
        CreateSpiritsMetadata.save(category, items)

        formatted_response: ResponseFormat = await return_formatter(
            "success",
            status.HTTP_201_CREATED,
            None,
            "Metadata registration successful",
        )

    except Exception as e:
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Metadata registration failed: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.get(
    "/spirits/metadata/{category}", summary="주류 정보 메타데이터 조회", tags=["주류"]
)
async def spirits_metadata_details(
    category: Annotated[
        SpiritsMetadataCategory, Path(..., description="메타데이터 카테고리")
    ],
) -> ORJSONResponse:
    metadata: list[dict[str, int | str]] = ReadSpiritsMetadata.based_on_category(
        category
    )

    formatted_response: ResponseFormat = await return_formatter(
        "success", status.HTTP_200_OK, metadata, "Successfully get metadata"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@app.delete(
    "/spirits/metadata/{id}", summary="주류 정보 메타데이터 삭제", tags=["주류"]
)
async def spirits_metadata_remover(
    id: Annotated[int, Path(..., description="메타데이터 인덱스")],
) -> ORJSONResponse:
    try:
        DeleteSpiritsMetadata.remove(id)
        formatted_response: ResponseFormat = await return_formatter(
            "success", status.HTTP_200_OK, None, "Successfully delete metadata"
        )

    except HTTPException as he:
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
    except Exception as e:
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to delete metadata: {e!s}",
        )

    return ORJSONResponse(
        content=formatted_response, status_code=formatted_response["code"]
    )


@app.get("/version", summary="서비스 버전 확인")
async def version() -> ORJSONResponse:
    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, {"version": app.version}, "Successfully get version"
    )

    return ORJSONResponse(formatted_response, status.HTTP_200_OK)

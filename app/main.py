from asyncio import set_event_loop_policy as set_global_asyncio_event_loop_policy
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Body,
    FastAPI,
    File,
    Form,
    # Header,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from structlog import BoundLogger
from uvloop import EventLoopPolicy as uvloopEventLoopPolicy

from auth import VerifyToken, refresh_access_token, sign_in_token
from model import (
    COCKTAIL_DATA_KIND,
    IngredientDict,
    LiqueurDict,
    LiqueurSearch,
    Login,
    MetadataCategory,
    MetadataRegister,
    ResponseFormat,
    SearchResponse,
    SpiritsDict,
    SpiritsSearch,
    User,
)
from model.validation import (
    ImageValidation,
    MetadataValidation,
)
from query import queries
from utils import Logger, return_formatter

set_global_asyncio_event_loop_policy(uvloopEventLoopPolicy())

logger: BoundLogger = Logger().setup()

cocktail_maker = FastAPI(
    title="Cocktail maker REST API",
    # semantic-versioning: major.minor.patch[-build]
    version="0.1.0-dev",
    summary="칵테일 제조법과 주류 및 재료 정보 제공",
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
    ],
    default_response_class=ORJSONResponse,
    docs_url="/api/docs",
)

"""
Preflight is OPTIONS method
This request occurs when resources on the server may change

PUT, DELETE, PATCH: mandatory for preflight requests
POST: preflight requests were made except for "text/plain", "application/x-www-form-urlencoded", "multipart/form-data"
"""
cocktail_maker.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",  # bearer token
        "Accept-Encoding",  # encoding (gzip, deflate)
        "Origin",  # origin of request
        "X-Requested-With",  # ajax request identification
        "User-Agent",  # client information
        "Cache-Control",  # cache policy
    ],
    expose_headers=["X-Expire-Seconds"],
    max_age=3600,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 500  # 테스트 환경
REFRESH_TOKEN_EXPIRE_DAYS = 7

cocktail_maker_v1 = APIRouter(prefix="/api/v1")


@cocktail_maker_v1.post("/signup", summary="회원가입", tags=["인증"])
async def sign_up(user: Annotated[User, Body(...)]) -> Response:
    """
    회원가입과 동시에 로그인을 수행하므로, 회원가입 성공 시 메시지와 함께 JWT 를 반환
    """
    try:
        if not await queries.Users.sign_up(user):
            raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

        login = Login(
            userId=user.user_id,
            password=user.password,
        )
        if (roles := await queries.Users.sign_in(login)) == []:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid user_id or password"
            )

        jwt: dict[str, str] = sign_in_token(login.userId, roles)

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
        secure=True,  # HTTPS에서만 전송, Reverse Proxy 환경에서 'X-Forwarded-Proto' Header 추가 필요
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


@cocktail_maker_v1.post("/signin", summary="로그인", tags=["인증"])
async def sign_in(login: Annotated[Login, Body(...)]) -> Response:
    """
    로그인 성공 시 메시지와 함께 JWT 를 반환
    """
    try:
        if (roles := await queries.Users.sign_in(login)) == []:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid user_id or password"
            )

        jwt: dict[str, str] = sign_in_token(login.userId, roles)

        logger.info("User successfully logged in", user_id=login.userId, roles=roles)

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


@cocktail_maker_v1.post("/refresh-token", summary="액세스 토큰 갱신", tags=["인증"])
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


@cocktail_maker_v1.get("/version", summary="서비스 버전 확인", tags=["기타"])
async def version() -> ORJSONResponse:
    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, {"version": cocktail_maker.version}, "Successfully get version"
    )

    return ORJSONResponse(formatted_response, status.HTTP_200_OK)


@cocktail_maker_v1.get("/health", summary="상태 확인", tags=["기타"])
async def health_check() -> ORJSONResponse:
    """
    서비스 상태 확인
    """
    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, {"status": "ok"}, "Service is running"
    )

    return ORJSONResponse(
        formatted_response, status.HTTP_200_OK, headers={"X-Expire-Seconds": "30"}
    )


@cocktail_maker_v1.post(
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
    originNation: Annotated[str, Form(...)],
    originLocation: Annotated[str, Form(...)],
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

        # 메타데이터 검증, 모든 params 가 주어질 경우 모두 응답이 옴
        listed_taste, listed_aroma, listed_finish = MetadataValidation(
            "spirits",
            taste,
            aroma,
            finish,
        )()

        item: SpiritsDict = SpiritsDict(
            name=name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=kind,
            sub_kind=subKind,
            amount=amount,
            alcohol=alcohol,
            origin_nation=originNation,
            origin_location=originLocation,
            description=description,
            created_at=datetime.now(tz=UTC),
        )
        data: str = await queries.CreateSpirits(
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


@cocktail_maker_v1.put(
    "/spirits/{document_id}", summary="주류 정보 수정", tags=["주류"]
)
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
    originNation: Annotated[str, Form(...)],
    originLocation: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    mainImage: Annotated[
        UploadFile,
        File(..., description="주류의 대표 이미지, 최대 2MB"),
    ],
    subImage1: Annotated[UploadFile | None, File()] = None,
    subImage2: Annotated[UploadFile | None, File()] = None,
    subImage3: Annotated[UploadFile | None, File()] = None,
    subImage4: Annotated[UploadFile | None, File()] = None,
) -> Response:
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
        listed_taste, listed_aroma, listed_finish = MetadataValidation(
            "spirits", taste, aroma, finish
        )()

        item: SpiritsDict = SpiritsDict(
            name=name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=kind,
            sub_kind=subKind,
            amount=amount,
            alcohol=alcohol,
            origin_nation=originNation,
            origin_location=originLocation,
            description=description,
            updated_at=datetime.now(tz=UTC),
        )
        await queries.UpdateSpirits(
            document_id,
            item,
            read_main_image,
            read_sub_image1,
            read_sub_image2,
            read_sub_image3,
            read_sub_image4,
        ).update()

        logger.info("Spirits successfully registered", name=name)

        response = Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as he:
        logger.error("Failed to update spirits", code=he.status_code, message=he.detail)
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
        response = Response(formatted_response, formatted_response["code"])
    except Exception as e:
        logger.error("Failed to update spirits", error=str(e))
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to update spirits: {e!s}",
        )
        response = Response(formatted_response, formatted_response["code"])

    return response


@cocktail_maker_v1.get("/spirits/{name}", summary="단일 주류 정보 조회", tags=["주류"])
async def spirits_detail(
    name: Annotated[str, Path(..., description="주류의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await queries.RetrieveSpirits(name).only_name()

    formatted_response: ResponseFormat = await return_formatter(
        "success", status.HTTP_200_OK, spirits, "Successfully get spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get("/spirits", summary="주류 정보 검색", tags=["주류"])
async def spirits_search(
    params: Annotated[SpiritsSearch, Query(...)],
    _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    data: SearchResponse = await queries.SearchSpirits(params).query()

    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, data, "Successfully search spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.delete("/spirits/{id}", summary="주류 정보 삭제", tags=["주류"])
async def spirits_remover(
    id: Annotated[str, Path(...)],
) -> ORJSONResponse:
    await queries.DeleteSpirits(id).remove()

    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, None, "Successfully delete spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.post(
    "/metadata/{kind}/{category}",
    summary="메타데이터 등록",
    tags=["메타데이터"],
)
async def metadata_register(
    kind: Annotated[COCKTAIL_DATA_KIND, Path(..., description="메타데이터 종류")],
    category: Annotated[MetadataCategory, Path(..., description="메타데이터 카테고리")],
    items: Annotated[MetadataRegister, Body(...)],
) -> ORJSONResponse:
    try:
        queries.Metadata.create(category, items, kind)

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


@cocktail_maker_v1.get(
    "/metadata/{kind}/{category}", summary="메타데이터 조회", tags=["메타데이터"]
)
async def metadata_details(
    kind: Annotated[COCKTAIL_DATA_KIND, Path(..., description="메타데이터 종류")],
    category: Annotated[MetadataCategory, Path(..., description="메타데이터 카테고리")],
    # Header 표준 값
    # authorization: Annotated[str | None, Header(alias="Authorization")] = None,
    # date: Annotated[str | None, Header(alias="Date")] = None,
    # if_modified_since: Annotated[str | None, Header(alias="If-Modified-Since")] = None,
    # forwarded: Annotated[str | None, Header(alias="Forwarded")] = None,
) -> ORJSONResponse:
    # print(f"authorization: {authorization}")
    # print("date: ", date)
    # print("if_modified_since: ", if_modified_since)
    # print("forwarded: ", forwarded)
    metadata: list[dict[str, int | str]] = queries.Metadata.read(category, kind)

    formatted_response: ResponseFormat = await return_formatter(
        "success", status.HTTP_200_OK, metadata, "Successfully get metadata"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.delete(
    "/metadata/{id}", summary="메타데이터 삭제", tags=["메타데이터"]
)
async def metadata_remover(
    id: Annotated[int, Path(..., description="메타데이터 인덱스")],
) -> ORJSONResponse:
    try:
        queries.Metadata.delete(id)
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


@cocktail_maker_v1.post(
    "/liqueur",
    summary="리큐르 정보 등록",
    tags=["리큐르"],
)
async def liqueur_register(  # noqa: PLR0913
    name: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="이름",
        ),
    ],
    brand: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="브랜드",
        ),
    ],
    taste: Annotated[
        list[str], Form(..., min_length=1, max_length=10, description="맛")
    ],
    kind: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="종류",
        ),
    ],
    subKind: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="세부 종류",
        ),
    ],
    mainIngredients: Annotated[
        list[str], Form(..., min_length=1, description="주재료")
    ],
    volume: Annotated[
        Decimal, Form(..., ge=0, le=10000, decimal_places=2, description="용량(mL)")
    ],
    abv: Annotated[
        Decimal, Form(..., ge=0, le=100, decimal_places=2, description="도수")
    ],
    originNation: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="원산지 국가",
        ),
    ],
    description: Annotated[
        str, Form(..., min_length=1, max_length=1000, description="설명")
    ],
    mainImage: Annotated[
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
    ],
) -> ORJSONResponse:
    """
    단일 리큐르 정보 등록
    """
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(mainImage, [])

        # 메타데이터 검증
        listed_taste, _, _ = MetadataValidation("liqueur", taste)()

        item: LiqueurDict = LiqueurDict(
            name=name,
            brand=brand,
            taste=listed_taste,
            kind=kind,
            sub_kind=subKind,
            main_ingredients=mainIngredients,
            volume=float(volume),
            abv=float(abv),
            origin_nation=originNation,
            description=description,
            created_at=datetime.now(tz=UTC),
        )

        data: str = await queries.CreateLiqueur(
            item,
            read_main_image,
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


@cocktail_maker_v1.get(
    "/liqueur/{name}", summary="단일 리큐르 정보 조회", tags=["주류"]
)
async def liqueur_detail(
    name: Annotated[str, Path(..., description="리큐르의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await queries.RetrieveLiqueur(name).only_name()

    formatted_response: ResponseFormat = await return_formatter(
        "success", status.HTTP_200_OK, spirits, "Successfully get liqueur"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get("/liqueur", summary="리큐르 정보 검색", tags=["주류"])
async def liqueur_search(
    params: Annotated[LiqueurSearch, Query(...)],
    _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    data: SearchResponse = await queries.SearchLiqueur(params).query()

    formatted_response: ResponseFormat = await return_formatter(
        "success", 200, data, "Successfully search spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.put(
    "/liqueur/{document_id}", summary="리큐르 정보 수정", tags=["리큐르"]
)
async def liqueur_update(  # noqa: PLR0913
    document_id: Annotated[str, Path(..., min_length=24, max_length=24)],
    name: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="이름",
        ),
    ],
    brand: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="브랜드",
        ),
    ],
    taste: Annotated[
        list[str], Form(..., min_length=1, max_length=10, description="맛")
    ],
    kind: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="종류",
        ),
    ],
    subKind: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="세부 종류",
        ),
    ],
    mainIngredients: Annotated[
        list[str], Form(..., min_length=1, description="주재료")
    ],
    volume: Annotated[
        Decimal, Form(..., ge=0, le=10000, decimal_places=2, description="용량(mL)")
    ],
    abv: Annotated[
        Decimal, Form(..., ge=0, le=100, decimal_places=2, description="도수")
    ],
    originNation: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="원산지 국가",
        ),
    ],
    description: Annotated[
        str, Form(..., min_length=1, max_length=1000, description="설명")
    ],
    mainImage: Annotated[
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
    ],
) -> Response:
    """
    주류 정보 수정
    """
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(mainImage, [])

        # 메타데이터 검증
        listed_taste, _, _ = MetadataValidation("liqueur", taste)()

        item: LiqueurDict = LiqueurDict(
            name=name,
            brand=brand,
            taste=listed_taste,
            kind=kind,
            sub_kind=subKind,
            main_ingredients=mainIngredients,
            volume=float(volume),
            abv=float(abv),
            origin_nation=originNation,
            description=description,
            updated_at=datetime.now(tz=UTC),
        )
        # await queries.UpdateSpirits(
        #     document_id,
        #     item,
        #     read_main_image,
        #     read_sub_image1,
        #     read_sub_image2,
        #     read_sub_image3,
        #     read_sub_image4,
        # ).update()

        logger.info("Liqueur successfully registered", name=name)

        response = Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as he:
        logger.error("Failed to update spirits", code=he.status_code, message=he.detail)
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
        response = Response(formatted_response, formatted_response["code"])
    except Exception as e:
        logger.error("Failed to update spirits", error=str(e))
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to update spirits: {e!s}",
        )
        response = Response(formatted_response, formatted_response["code"])

    return response


@cocktail_maker_v1.post(
    "/ingredient",
    summary="기타 재료 정보 등록",
    tags=["기타 재료"],
)
async def ingredient_register(
    name: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=100,
            pattern="^[가-힣\\s]+$",
            description="이름",
        ),
    ],
    kind: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=50,
            pattern="^[가-힣\\s]+$",
            description="종류",
        ),
    ],
    description: Annotated[
        str, Form(..., min_length=1, max_length=1000, description="설명")
    ],
    mainImage: Annotated[
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
    ],
    brand: Annotated[
        list[str] | None,
        Form(
            min_length=1,
            max_length=10,
            description="브랜드",
        ),
    ] = None,
) -> ORJSONResponse:
    """
    단일 기타 재료 정보 등록
    """
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(mainImage, [])

        item: IngredientDict = IngredientDict(
            name=name,
            brand=brand,
            kind=kind,
            description=description,
            created_at=datetime.now(tz=UTC),
        )

        data: str = await queries.CreateIngredient(
            item,
            read_main_image,
        ).save()

        logger.info("Ingredient successfully registered", name=name)

        formatted_response: ResponseFormat = await return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register ingredient"
        )

    except HTTPException as he:
        logger.error(
            "Failed to register ingredient", code=he.status_code, message=he.detail
        )
        formatted_response = await return_formatter(
            "failed", he.status_code, None, he.detail
        )
    except Exception as e:
        logger.error("Failed to register ingredient", error=str(e))
        formatted_response = await return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to register ingredient: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


cocktail_maker.include_router(cocktail_maker_v1)

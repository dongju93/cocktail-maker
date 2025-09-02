from asyncio import set_event_loop_policy as set_global_asyncio_event_loop_policy
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from os import environ
from time import time_ns
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
    Security,
    status,
)
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse
from pyinstrument import Profiler
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette_compress import CompressMiddleware
from structlog import BoundLogger
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
    get_all_cors_headers,
    init,
)
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import emailpassword, session
from uvloop import EventLoopPolicy as uvloopEventLoopPolicy

from auth import (
    ProductionAPIKeyGenerator,
    VerifyToken,
    refresh_access_token,
    sign_in_token,
)
from model import (
    COCKTAIL_DATA_KIND,
    ApiKeyPublish,
    CocktailDict,
    CocktailRegisterForm,
    IngredientDict,
    IngredientRegisterForm,
    IngredientSearch,
    IngredientUpdateForm,
    LiqueurDict,
    LiqueurRegisterForm,
    LiqueurSearchQuery,
    LiqueurUpdateForm,
    Login,
    MetadataCategory,
    MetadataRegister,
    RecipeDict,
    RecipeStepDict,
    ResponseFormat,
    SearchResponse,
    SpiritsDict,
    SpiritsRegisterForm,
    SpiritsSearch,
    SpiritsUpdateForm,
    User,
)
from model.validation import ImageValidation
from query import metadata, queries
from utils import Logger, problem_details_formatter, return_formatter

init(
    app_info=InputAppInfo(
        app_name="cocktail-maker",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        api_base_path="/auth",
        website_base_path="/auth",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri="http://localhost:3567",
        api_key="73a50f5ae216404588bbbcee4f05b143",
    ),
    framework="fastapi",
    recipe_list=[
        session.init(),
        emailpassword.init(),
    ],
    mode="asgi",  # wsgi
)

set_global_asyncio_event_loop_policy(uvloopEventLoopPolicy())

load_dotenv()
logger: BoundLogger = Logger().setup()

SUPERTOKEN_API_KEY: str = environ["SUPERTOKEN_API_KEY"]

cocktail_maker = FastAPI(
    title="Cocktail maker REST API",
    # semantic-versioning: major.minor.patch[-build]
    version="0.1.0-dev",
    summary="칵테일 제조법과 주류 및 재료 정보 제공",
    description="""
    A comprehensive API for managing cocktail recipes, spirits, liqueurs, and ingredients.

    ## Features
    - **Spirits Management**: CRUD operations for alcoholic beverages
    - **Liqueur Management**: Complete liqueur database with metadata
    - **Ingredient Tracking**: Non-alcoholic cocktail ingredients
    - **Metadata System**: Taste profiles, aromas, and finish characteristics
    - **User Authentication**: JWT-based auth with role-based access control

    ## Authentication
    All endpoints except `/health` require authentication. Use `/auth` endpoints for login.
    """,
    contact={
        "name": "Cocktail Maker Team",
        "email": "team@cocktail-maker.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
        {"url": "https://api.cocktail-maker.com", "description": "Production server"},
    ],
    default_response_class=ORJSONResponse,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@cocktail_maker.middleware("http")
async def profile_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    성능 프로파일링 미들웨어

    쿼리 파라미터 ?profile=true로 요청 시 해당 요청의 성능 프로파일을 HTML로 반환

    Profiler 설정 옵션:
    - interval (float, 기본값: 0.001): 샘플링 간격 (초)
      * 작은 값 (0.0001): 높은 정확도, 높은 오버헤드
      * 큰 값 (0.01): 낮은 오버헤드, 낮은 정확도

    - async_mode (AsyncMode, 기본값: "enabled"): async/await 추적 모드
      * "enabled": await 지점에서 대기 시간 추적, 실제 코드 실행 시간만 측정 (권장)
      * "disabled": async/await 지원 없이 모든 실행 추적 (이벤트 루프, 다른 코루틴 포함)
      * "strict": 현재 async context만 엄격하게 프로파일링, 다른 context는 <out-of-context>로 표시

    - use_timing_thread (bool | None, 기본값: None): 별도 타이밍 스레드 사용 여부
      * True: 시간 측정 오버헤드가 큰 시스템에서 성능 향상을 위해 별도 스레드 사용
      * False: 메인 스레드에서 시간 측정
      * None: pyinstrument가 자동으로 최적 방법 선택

    프로파일링 출력 형식:
    - output_html(): 대화형 HTML 출력 (웹 브라우저에서 확인, 트리 구조 탐색 가능)
    - output_text(): 콘솔용 텍스트 출력 (터미널에서 확인, 간단한 텍스트 형태)
    - write_html(path): HTML 파일로 저장 (파일 시스템에 저장 후 나중에 확인)
    - open_in_browser(): 웹 브라우저에서 자동 열기 (즉시 시각화된 결과 확인)
    - print(): 콘솔에 직접 출력 (실시간 결과 확인)

    텍스트 출력 옵션:
    - unicode: 유니코드 문자 사용 여부 (트리 구조 표시용)
    - color: 컬러 출력 여부 (터미널 색상 지원 시)
    - show_all: 모든 함수 표시 여부 (기본적으로 빠른 함수는 숨김)
    - timeline: 타임라인 뷰 표시 여부 (시간 흐름에 따른 실행 순서)
    - time: 시간 표시 형식 ("seconds" 또는 "percent_of_total")
    - flat: 플랫 뷰 표시 여부 (호출 스택 대신 함수별 총 시간)
    - short_mode: 간단 모드 (요약된 출력)

    Args:
        request: FastAPI 요청 객체
        call_next: 다음 미들웨어 또는 엔드포인트 호출 함수

    Returns:
        HTMLResponse: 프로파일링 결과 HTML (profile=true인 경우)
        Response: 일반 응답 (profile=false 또는 없는 경우)

    Examples:
        # 기본 프로파일링 활성화
        GET /api/v1/health?profile=true

        # 고정밀 프로파일링 (짧은 함수 분석용)
        profiler = Profiler(interval=0.0001, async_mode="enabled")

        # 저오버헤드 프로파일링 (긴 실행 시간용)
        profiler = Profiler(interval=0.01, async_mode="disabled")

        # 엄격한 async context 프로파일링
        profiler = Profiler(interval=0.001, async_mode="strict")

        # 다양한 출력 방식 지원
        1. HTML로 브라우저에서 확인
        profiler.open_in_browser()

        2. 파일로 저장
        profiler.write_html("profile_result.html")

        3. 콘솔에 텍스트로 출력
        profiler.print(color=True, unicode=True)
        - 콘솔 출력 옵션
          * unicode: 유니코드 문자 사용 (트리 구조 표시용)
          * color: 컬러 출력 (터미널 색상 지원 시)
          * show_all: 모든 함수 표시 (기본적으로 빠른 함수는 숨김)
          * timeline: 타임라인 뷰 표시 (시간 흐름에 따른 실행 순서)
          * time: 시간 표시 형식 ("seconds" 또는 "percent_of_total")
          * flat: 트리 구조로 호출 스택 표시
          * short_mode: 간단 모드 (요약된 출력)

        4. 문자열로 가져와서 로그에 기록
        text_output = profiler.output_text(color=False)
        logger.info(f"Profile result:\n{text_output}")
    """
    profiling: bool = request.query_params.get("profile") == "true"

    if profiling:
        with Profiler() as profiler:
            response: Response = await call_next(request)

        # Console output
        profiler.print(
            color=True,
            unicode=True,
            show_all=False,
            timeline=True,
            flat=False,
            short_mode=True,
            time="percent_of_total",
        )

        # File write
        # # 파일명에 번호 추가 로직
        # base_filename = "profile.speedscope"
        # extension = ".json"
        # filename = f"{base_filename}-0{extension}"
        # counter = 0

        # # 파일이 존재하면 번호를 증가시켜 새로운 파일명 생성
        # while PathLib(filename).exists():
        #     counter += 1
        #     filename = f"{base_filename}-{counter}{extension}"

        # async with aiofiles.open(filename, "w") as out:
        #     await out.write(profiler.output(renderer=SpeedscopeRenderer()))

        # HTML view
        # return HTMLResponse(profiler.output_html())
        return response
    else:
        return await call_next(request)


# cocktail_maker.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_origins=["http://localhost:5173"],
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

"""
Preflight is OPTIONS method
This request occurs when resources on the server may change

PUT, DELETE, PATCH: mandatory for preflight requests
POST: preflight requests were made except for "text/plain", "application/x-www-form-urlencoded", "multipart/form-data"
"""
# cocktail_maker.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_origins=[
#         "http://localhost:5173",
#     ],
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=[  # Headers that API server accepts
#         "Authorization",  # bearer token, e.g. Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
#         "Accept-Encoding",  # encoding,  e.g. gzip, deflate, br
#         "Origin",  # origin of request, e.g. http://localhost:5173
#         "X-Requested-With",  # ajax request identification, e.g. XMLHttpRequest
#         "User-Agent",  # client information, e.g. Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...
#         "Cache-Control",  # cache policy, e.g. no-cache, no-store, must-revalidate
#     ],
#     expose_headers=[
#         "X-Server-Version",
#     ],  # Headers that client can see and access via JavaScript
#     # max_age=3600,  # Preflight cache duration in seconds
# )


# SecWeb(
#     app=cocktail_maker,  # Pass FastAPI application instance to SecWeb
#     Option={  # Dictionary containing security header configurations
#         "csp": {  # Content Security Policy configuration
#             "default-src": ["'self'"],  # Allow resources only from same origin
#             "script-src": [
#                 "'self'",
#                 "'unsafe-inline'",
#                 # "'unsafe-eval'",
#                 "https://cdn.jsdelivr.net",
#             ],  # Allow scripts from self, inline scripts, and eval() - development only
#             "style-src": [
#                 "'self'",
#                 # "'unsafe-inline'",
#                 "https://cdn.jsdelivr.net",
#             ],  # Allow styles from self and inline styles - development only
#             "img-src": [
#                 "'self'",
#                 "data:",
#                 "blob:",
#                 "https:",
#             ],  # Allow images from self, data URLs, blob URLs, and HTTPS sources
#             "font-src": ["'self'", "data:"],  # Allow fonts from self and data URLs
#             "connect-src": [
#                 "'self'",
#                 "http://localhost:5173",
#                 "ws://localhost:5173",
#             ],  # Allow connections to self and development server (HTTP/WebSocket)
#             "media-src": [
#                 "'self'",
#                 "blob:",
#             ],  # Allow media files from self and blob URLs
#             "object-src": [
#                 "'none'"
#             ],  # Disallow all object sources (<object>, <embed>, <applet> tags)
#             "base-uri": ["'self'"],  # Allow <base> tag to reference only same origin
#             "form-action": ["'self'"],  # Allow form submissions only to same origin
#             "frame-ancestors": [
#                 "'none'"
#             ],  # Prevent this page from being embedded in frames/iframes
#         },
#         "hsts": {
#             "max-age": 31536000,
#             "includeSubDomains": True,
#             "preload": True,
#         },  # HTTP Strict Transport Security: 1 year max-age, include subdomains, enable preload
#         "referrer": [
#             "strict-origin-when-cross-origin"
#         ],  # Referrer Policy: send full URL for same-origin, only origin for cross-origin requests
#         "xcto": True,  # X-Content-Type-Options: nosniff - prevent MIME type sniffing attacks
#         "xframe": "DENY",  # X-Frame-Options: DENY - prevent clickjacking by blocking iframe embedding
#         "cacheControl": {
#             "max-age": 10,  # Seconds
#             "private": True,  # Cache only in browser, not shared caches
#         },
#         # "cacheControl": {
#         #     "no-store": True
#         # },  # Cache-Control: no-store - prevent caching of responses
#         "xss": True,  # X-XSS-Protection: enable XSS filtering (legacy header, mostly deprecated)
#         "xdns": "off",  # X-DNS-Prefetch-Control: off - disable DNS prefetching for privacy
#         "xcdp": "none",  # X-Permitted-Cross-Domain-Policies: none - block Adobe Flash/PDF cross-domain requests
#         "xdo": True,  # X-Download-Options: noopen - prevent Internet Explorer from opening downloads in security context
#         "oac": True,  # Origin-Agent-Cluster: ?1 - isolate agent cluster by origin for better security
#         "corp": "cross-origin",  # Cross-Origin-Resource-Policy: same-origin - prevent cross-origin resource sharing, e.g. cross-origin, same-origin, same-site
#         "coop": "unsafe-none",  # Cross-Origin-Opener-Policy: same-origin - prevent cross-origin window references, e.g. same-origin, same-origin-allow-popups, unsafe-none
#         "coep": "require-corp",  # Cross-Origin-Embedder-Policy: require-corp - require CORP header for cross-origin resources, e.g. require-corp, credentialless, unsafe-none
#     },
#     Routes=[],  # List of routes for Clear-Site-Data header (empty - not using this feature)
#     script_nonce=False,  # Disable automatic nonce generation for script tags in CSP
#     style_nonce=False,  # Disable automatic nonce generation for style tags in CSP
#     report_only=False,  # Disable CSP Report-Only mode - enforce policies instead of just reporting violations
# )


@cocktail_maker.middleware("http")
async def add_custom_headers(request: Request, call_next):  # noqa: ANN001, ANN201
    response = await call_next(request)

    # Application global custom headers
    response.headers["X-Server-Version"] = cocktail_maker.version

    # Security headers
    # response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["X-Frame-Options"] = "DENY"
    # response.headers["X-XSS-Protection"] = "1; mode=block"
    # response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # Content Security Policy for API
    # response.headers["Content-Security-Policy"] = (
    #     "default-src 'self'; "
    #     "script-src 'self'; "
    #     "style-src 'self' 'unsafe-inline'; "
    #     "img-src 'self' data: https:; "
    #     "font-src 'self'; "
    #     "connect-src 'self'; "
    #     "media-src 'none'; "
    #     "object-src 'none'; "
    #     "base-uri 'self'; "
    #     "form-action 'self'; "
    #     "frame-ancestors 'none'"
    # )

    return response


cocktail_maker.add_middleware(
    CompressMiddleware, minimum_size=1, zstd_level=4, brotli_quality=4, gzip_level=6
)

cocktail_maker.add_middleware(get_middleware())

# Add security middleware
cocktail_maker.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.cocktail-maker.com"],
)

cocktail_maker.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", *get_all_cors_headers()],
)


@cocktail_maker.exception_handler(Exception)
async def general_exception_handler_rfc(
    request: Request, exc: Exception
) -> ORJSONResponse:
    """General exception handler for server errors using RFC 9457 format"""
    logger.error("Unhandled server error", error=str(exc), path=request.url.path)

    problem_details = problem_details_formatter(
        status=500,
        title="Internal Server Error",
        detail="An unexpected error occurred while processing the request",
        type_uri="https://httpstatuses.com/500",
    )

    return ORJSONResponse(
        content=problem_details, status_code=500, media_type="application/problem+json"
    )


@cocktail_maker.exception_handler(StarletteHTTPException)
async def http_exception_handler_rfc(
    request: Request, exc: StarletteHTTPException
) -> Response:
    """Handle FastAPI HTTPExceptions with RFC 9457 format"""

    if exc.status_code >= status.HTTP_400_BAD_REQUEST:
        if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error(
                "HTTP server error",
                code=exc.status_code,
                detail=exc.detail,
                path=request.url.path,
            )
            title = f"Server Error {exc.status_code}"
        else:
            logger.warning(
                "HTTP client error",
                code=exc.status_code,
                detail=exc.detail,
                path=request.url.path,
            )
            title = f"Client Error {exc.status_code}"

        problem_details = problem_details_formatter(
            status=exc.status_code,
            title=title,
            detail=exc.detail,
            type_uri=f"https://httpstatuses.com/{exc.status_code}",
        )

        return ORJSONResponse(
            content=problem_details,
            status_code=exc.status_code,
            media_type="application/problem+json",
        )

    return await http_exception_handler(request, exc)


ACCESS_TOKEN_EXPIRE_MINUTES = 500  # 테스트 환경
REFRESH_TOKEN_EXPIRE_DAYS = 7

cocktail_maker_v1 = APIRouter(prefix="/api/v1")


@cocktail_maker_v1.post("/signup", summary="회원가입", tags=["인증"])
async def sign_up(user: Annotated[User, Body(...)]) -> Response:
    """회원가입과 동시에 로그인을 수행하므로, 회원가입 성공 시 메시지와 함께 JWT 를 반환

    Args:
        user (Annotated[User, Body): 회원가입에 필요한 사용자 정보

    Raises:
        HTTPException: 409 - 이미 존재하는 사용자인 경우
        HTTPException: 401 - 회원가입 후 로그인 검증에 실패한 경우

    Returns:
        Response:
            - 성공 시: 204 No Content, JWT 토큰이 쿠키로 설정됨
                - accessToken: httponly 쿠키 (15분 만료)
                - refreshToken: httponly 쿠키 (7일 만료, /refresh-token 경로 제한)
            - 실패 시: 해당 상태 코드와 에러 메시지가 포함된 JSON 응답
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
            return_formatter("failed", he.status_code, None, he.detail),
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
    """로그인

    Args:
        login (Annotated[Login, Body): 로그인 정보

    Raises:
        HTTPException: 로그인 실패 시

    Returns:
        Response: 로그인 성공 시 JWT 쿠키 설정
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
            return_formatter("failed", he.status_code, None, he.detail),
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
    """액세스 토큰 갱신

    Args:
        request (Request): 요청 객체

    Raises:
        HTTPException: 리프레시 토큰이 없는 경우

    Returns:
        Response: 204 No Content
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
            return_formatter("failed", he.status_code, None, he.detail),
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


@cocktail_maker_v1.get("/my-role", summary="내 JWT 권한 확인", tags=["인증"])
async def my_role(
    _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    """현재 로그인된 사용자의 권한 확인

    Args:
        _ (Annotated[None, Security]): 보안 검증을 위한 필드

    Returns:
        ORJSONResponse: 사용자 권한 정보
    """
    formatted_response: ResponseFormat = return_formatter(
        "success", 200, {"roles": ["admin", "user"]}, "Successfully get user roles"
    )

    return ORJSONResponse(formatted_response, status.HTTP_200_OK)


@cocktail_maker_v1.post("/publish-api-key", summary="API 키 발급", tags=["인증"])
async def publish_api_key(
    api_key_publish: Annotated[ApiKeyPublish, Body(...)],
    _: Annotated[None, Security(VerifyToken(["admin"]))],
) -> ORJSONResponse:
    generator: ProductionAPIKeyGenerator = ProductionAPIKeyGenerator.from_env()
    api_key: str = generator.generate_api_key(api_key_publish.domain, time_ns())

    return ORJSONResponse(
        return_formatter(
            "success", 200, {"api_key": api_key}, "API key generated successfully"
        )
    )


@cocktail_maker_v1.get("/health", summary="상태 확인", tags=["기타"])
async def health_check() -> ORJSONResponse:
    """
    서비스 상태 확인
    """
    formatted_response: ResponseFormat = return_formatter(
        "success", 200, {"status": "ok"}, "Service is running"
    )

    return ORJSONResponse(formatted_response, status.HTTP_200_OK)


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
async def spirits_register(
    form: Annotated[SpiritsRegisterForm, Form()],
) -> ORJSONResponse:
    """
    단일 주류 정보 등록
    """

    SPIRITS_REGISTER_FAILURE_MESSAGE = "Failed to register spirits"

    try:
        # 이미지 검증 및 변환
        read_main_image, sub_images_bytes = await ImageValidation.files(
            form.main_image,
            [form.sub_image1, form.sub_image2, form.sub_image3, form.sub_image4],
        )
        read_sub_image1, read_sub_image2, read_sub_image3, read_sub_image4 = (
            sub_images_bytes
        )

        # 메타데이터 검증
        validate_metadata = metadata.MetadataValidation(
            "spirits",
            form.taste,
            form.aroma,
            form.finish,
        )
        listed_taste, listed_aroma, listed_finish = validate_metadata()

        item: SpiritsDict = SpiritsDict(
            name=form.name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=form.kind,
            sub_kind=form.sub_kind,
            amount=form.amount,
            alcohol=form.alcohol,
            origin_nation=form.origin_nation,
            origin_location=form.origin_location,
            description=form.description,
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

        logger.info("Spirits successfully registered", name=form.name)

        formatted_response: ResponseFormat = return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register spirits"
        )

    except HTTPException as he:
        logger.error(
            SPIRITS_REGISTER_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        logger.error(SPIRITS_REGISTER_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{SPIRITS_REGISTER_FAILURE_MESSAGE}: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.put(
    "/spirits/{document_id}", summary="주류 정보 수정", tags=["주류"]
)
async def spirits_update(
    document_id: Annotated[str, Path(description="주류의 문서 ID")],
    form: Annotated[SpiritsUpdateForm, Form()],
) -> Response:
    """
    주류 정보 수정
    """

    SPIRITS_UPDATE_FAILURE_MESSAGE = "Failed to update spirits"

    try:
        # 이미지 검증 및 변환
        read_main_image, sub_images_bytes = await ImageValidation.files(
            form.main_image,
            [form.sub_image1, form.sub_image2, form.sub_image3, form.sub_image4],
        )
        read_sub_image1, read_sub_image2, read_sub_image3, read_sub_image4 = (
            sub_images_bytes
        )

        # 메타데이터 검증
        validate_metadata = metadata.MetadataValidation(
            "spirits", form.taste, form.aroma, form.finish
        )
        listed_taste, listed_aroma, listed_finish = validate_metadata()

        item: SpiritsDict = SpiritsDict(
            name=form.name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            kind=form.kind,
            sub_kind=form.sub_kind,
            amount=form.amount,
            alcohol=form.alcohol,
            origin_nation=form.origin_nation,
            origin_location=form.origin_location,
            description=form.description,
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

        logger.info("Spirits successfully updated", name=form.name)

        response = Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as he:
        logger.error(
            SPIRITS_UPDATE_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
        response = Response(formatted_response, formatted_response["code"])
    except Exception as e:
        logger.error(SPIRITS_UPDATE_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{SPIRITS_UPDATE_FAILURE_MESSAGE}: {e!s}",
        )
        response = Response(formatted_response, formatted_response["code"])

    return response


@cocktail_maker_v1.get("/spirits/{name}", summary="단일 주류 정보 조회", tags=["주류"])
async def spirits_detail(
    name: Annotated[str, Path(..., description="주류의 이름, 정확한 일치")],
    # _: Annotated[SessionContainer, Depends(verify_session())],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await queries.RetrieveSpirits(name).only_name()

    formatted_response: ResponseFormat = return_formatter(
        "success", status.HTTP_200_OK, spirits, "Successfully get spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get("/spirits", summary="주류 정보 검색", tags=["주류"])
async def spirits_search(
    params: Annotated[SpiritsSearch, Depends()],
    # _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    data: SearchResponse = await queries.SearchSpirits(params).query()

    formatted_response: ResponseFormat = return_formatter(
        "success", 200, data, "Successfully search spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.delete("/spirits/{id}", summary="주류 정보 삭제", tags=["주류"])
async def spirits_remover(
    id: Annotated[str, Path(...)],
) -> ORJSONResponse:
    await queries.DeleteSpirits(id).remove()

    formatted_response: ResponseFormat = return_formatter(
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
    # // TODO: 중복된 항목만 등록 건너뛰기
    try:
        metadata.Metadata.create(category, items, kind)

        formatted_response: ResponseFormat = return_formatter(
            "success",
            status.HTTP_201_CREATED,
            None,
            "Metadata registration successful",
        )

    except Exception as e:
        formatted_response = return_formatter(
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
    metadata_list: list[dict[str, int | str]] = metadata.Metadata.read(category, kind)

    formatted_response: ResponseFormat = return_formatter(
        "success", status.HTTP_200_OK, metadata_list, "Successfully get metadata"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.delete(
    "/metadata/{id}", summary="메타데이터 삭제", tags=["메타데이터"]
)
async def metadata_remover(
    id: Annotated[int, Path(..., description="메타데이터 인덱스")],
) -> ORJSONResponse:
    try:
        metadata.Metadata.delete(id)
        formatted_response: ResponseFormat = return_formatter(
            "success", status.HTTP_200_OK, None, "Successfully delete metadata"
        )

    except HTTPException as he:
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        formatted_response = return_formatter(
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
async def liqueur_register(
    form: Annotated[LiqueurRegisterForm, Form()],
) -> ORJSONResponse:
    """
    단일 리큐르 정보 등록
    """
    LIQUEUR_REGISTER_FAILURE_MESSAGE = "Failed to register liqueur"

    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(form.main_image, [])

        # 메타데이터 검증
        validate_metadata = metadata.MetadataValidation("liqueur", form.taste)
        listed_taste, _, _ = validate_metadata()

        item: LiqueurDict = LiqueurDict(
            name=form.name,
            brand=form.brand,
            taste=listed_taste,
            kind=form.kind,
            sub_kind=form.sub_kind,
            main_ingredients=form.main_ingredients,
            volume=float(form.volume),
            abv=float(form.abv),
            origin_nation=form.origin_nation,
            description=form.description,
            created_at=datetime.now(tz=UTC),
        )

        data: str = await queries.CreateLiqueur(
            item,
            read_main_image,
        ).save()

        logger.info("Spirits successfully registered", name=form.name)

        formatted_response: ResponseFormat = return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register spirits"
        )

    except HTTPException as he:
        logger.error(
            LIQUEUR_REGISTER_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        logger.error(LIQUEUR_REGISTER_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{LIQUEUR_REGISTER_FAILURE_MESSAGE}: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get(
    "/liqueur/{name}", summary="단일 리큐르 정보 조회", tags=["주류"]
)
async def liqueur_detail(
    name: Annotated[str, Path(..., description="리큐르의 이름, 정확한 일치")],
) -> ORJSONResponse:
    spirits: dict[str, Any] = await queries.RetrieveLiqueur(name).only_name()

    formatted_response: ResponseFormat = return_formatter(
        "success", status.HTTP_200_OK, spirits, "Successfully get liqueur"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get("/liqueur", summary="리큐르 정보 검색", tags=["주류"])
async def liqueur_search(
    params: Annotated[LiqueurSearchQuery, Depends()],
    _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    data: SearchResponse = await queries.SearchLiqueur(params).query()

    formatted_response: ResponseFormat = return_formatter(
        "success", 200, data, "Successfully search spirits"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.put(
    "/liqueur/{document_id}", summary="리큐르 정보 수정", tags=["리큐르"]
)
async def liqueur_update(
    document_id: Annotated[str, Path(..., min_length=24, max_length=24)],
    form: Annotated[LiqueurUpdateForm, Form()],
) -> Response:
    """
    주류 정보 수정
    """
    LIQUEUR_UPDATE_FAILURE_MESSAGE = "Failed to update liqueur"
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(form.main_image, [])

        # 메타데이터 검증
        validate_metadata = metadata.MetadataValidation("liqueur", form.taste)
        listed_taste, _, _ = validate_metadata()

        liqueur_item: LiqueurDict = LiqueurDict(
            name=form.name,
            brand=form.brand,
            taste=listed_taste,
            kind=form.kind,
            sub_kind=form.sub_kind,
            main_ingredients=form.main_ingredients,
            volume=float(form.volume),
            abv=float(form.abv),
            origin_nation=form.origin_nation,
            description=form.description,
            updated_at=datetime.now(tz=UTC),
        )
        await queries.UpdateLiqueur(
            document_id,
            liqueur_item,
            read_main_image,
        ).update()

        logger.info("Liqueur successfully updated", name=form.name)

        response = Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as he:
        logger.error(
            LIQUEUR_UPDATE_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
        response = Response(formatted_response, formatted_response["code"])
    except Exception as e:
        logger.error(LIQUEUR_UPDATE_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{LIQUEUR_UPDATE_FAILURE_MESSAGE}: {e!s}",
        )
        response = Response(formatted_response, formatted_response["code"])

    return response


@cocktail_maker_v1.delete(
    "/liqueur/{document_id}", summary="리큐르 정보 삭제", tags=["리큐르"]
)
async def liqueur_remover(
    document_id: Annotated[str, Path(..., min_length=24, max_length=24)],
) -> ORJSONResponse:
    """
    리큐르 정보 삭제

    Args:
        document_id (str): 삭제할 리큐르의 MongoDB ObjectId

    Returns:
        ORJSONResponse: 삭제 성공/실패 응답
    """
    try:
        await queries.DeleteLiqueur(document_id).remove()

        logger.info("Liqueur successfully deleted", document_id=document_id)

        formatted_response: ResponseFormat = return_formatter(
            "success", 200, None, "Successfully delete liqueur"
        )

    except HTTPException as he:
        logger.error("Failed to delete liqueur", code=he.status_code, message=he.detail)
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        logger.error("Failed to delete liqueur", error=str(e))
        formatted_response = return_formatter(
            "failed", 500, None, f"Failed to delete liqueur: {e!s}"
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.post(
    "/ingredient",
    summary="기타 재료 정보 등록",
    tags=["기타 재료"],
)
async def ingredient_register(
    form: Annotated[IngredientRegisterForm, Form()],
) -> ORJSONResponse:
    """
    단일 기타 재료 정보 등록
    """
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(form.main_image, [])

        item: IngredientDict = IngredientDict(
            name=form.name,
            brand=form.brand,
            kind=form.kind,
            description=form.description,
            created_at=datetime.now(tz=UTC),
        )

        data: str = await queries.CreateIngredient(
            item,
            read_main_image,
        ).save()

        logger.info("Ingredient successfully registered", name=form.name)

        formatted_response: ResponseFormat = return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register ingredient"
        )

    except HTTPException as he:
        logger.error(
            "Failed to register ingredient", code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        logger.error("Failed to register ingredient", error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"Failed to register ingredient: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get(
    "/ingredient/{name}", summary="단일 기타 재료 정보 조회", tags=["기타 재료"]
)
async def ingredient_detail(
    name: Annotated[str, Path(..., description="기타 재료의 이름, 정확한 일치")],
) -> ORJSONResponse:
    ingredient: dict[str, Any] = await queries.RetrieveIngredient(name).only_name()

    formatted_response: ResponseFormat = return_formatter(
        "success", status.HTTP_200_OK, ingredient, "Successfully get ingredient"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.get("/ingredient", summary="기타 재료 정보 검색", tags=["기타 재료"])
async def ingredient_search(
    params: Annotated[IngredientSearch, Query()],
    _: Annotated[None, Security(VerifyToken(["admin", "user"]))],
) -> ORJSONResponse:
    data: SearchResponse = await queries.SearchIngredient(params).query()

    formatted_response: ResponseFormat = return_formatter(
        "success", 200, data, "Successfully search ingredients"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.put(
    "/ingredient/{document_id}", summary="기타 재료 정보 수정", tags=["기타 재료"]
)
async def ingredient_update(
    document_id: Annotated[str, Path(..., min_length=24, max_length=24)],
    form: Annotated[IngredientUpdateForm, Form()],
) -> Response:
    """
    기타 재료 정보 수정
    """
    INGREDIENT_UPDATE_FAILURE_MESSAGE = "Failed to update ingredient"
    try:
        # 이미지 검증 및 변환
        read_main_image, _ = await ImageValidation.files(form.main_image, [])

        item: IngredientDict = IngredientDict(
            name=form.name,
            brand=form.brand,
            kind=form.kind,
            description=form.description,
            updated_at=datetime.now(tz=UTC),
        )
        await queries.UpdateIngredient(
            document_id,
            item,
            read_main_image,
        ).update()

        logger.info("Ingredient successfully updated", name=form.name)

        response = Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as he:
        logger.error(
            INGREDIENT_UPDATE_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
        response = Response(formatted_response, formatted_response["code"])
    except Exception as e:
        logger.error(INGREDIENT_UPDATE_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{INGREDIENT_UPDATE_FAILURE_MESSAGE}: {e!s}",
        )
        response = Response(formatted_response, formatted_response["code"])

    return response


@cocktail_maker_v1.delete(
    "/ingredient/{document_id}", summary="기타 재료 정보 삭제", tags=["기타 재료"]
)
async def ingredient_remover(
    document_id: Annotated[str, Path(..., min_length=24, max_length=24)],
) -> ORJSONResponse:
    await queries.DeleteIngredient(document_id).remove()

    formatted_response: ResponseFormat = return_formatter(
        "success", 200, None, "Successfully delete ingredient"
    )

    return ORJSONResponse(formatted_response, formatted_response["code"])


@cocktail_maker_v1.post("/cocktail", summary="칵테일 정보 등록", tags=["칵테일"])
async def cocktail_register(
    form: Annotated[CocktailRegisterForm, Form()],
):
    COCKTAIL_REGISTER_FAILURE_MESSAGE = "Failed to register cocktail"
    try:
        # 이미지 검증 및 변환
        read_main_image, sub_images_bytes = await ImageValidation.files(
            form.main_image,
            [form.sub_image1, form.sub_image2, form.sub_image3, form.sub_image4],
        )
        read_sub_image1, read_sub_image2, read_sub_image3, read_sub_image4 = (
            sub_images_bytes
        )

        # 메타데이터 검증
        validate_metadata = metadata.MetadataValidation(
            "spirits",
            form.taste,
            form.aroma,
            form.finish,
        )
        listed_taste, listed_aroma, listed_finish = validate_metadata()

        item: CocktailDict = CocktailDict(
            name=form.name,
            aroma=listed_aroma,
            taste=listed_taste,
            finish=listed_finish,
            ingredients=[
                RecipeDict(
                    id=ingredient.id,
                    type=ingredient.type,
                    amount=ingredient.amount,
                    unit=ingredient.unit,
                )
                for ingredient in form.ingredients
            ],
            steps=[
                RecipeStepDict(step=step.step, description=step.description)
                for step in form.steps
            ],
            glass=form.glass,
            description=form.description,
            origin_nation=form.origin_nation,
            created_at=datetime.now(tz=UTC),
        )
        data: str = await queries.CreateCocktail(
            item,
            read_main_image,
            read_sub_image1,
            read_sub_image2,
            read_sub_image3,
            read_sub_image4,
        ).save()

        logger.info("Cocktail successfully registered", name=form.name)

        formatted_response: ResponseFormat = return_formatter(
            "success", status.HTTP_201_CREATED, data, "Successfully register cocktail"
        )

    except HTTPException as he:
        logger.error(
            COCKTAIL_REGISTER_FAILURE_MESSAGE, code=he.status_code, message=he.detail
        )
        formatted_response = return_formatter("failed", he.status_code, None, he.detail)
    except Exception as e:
        logger.error(COCKTAIL_REGISTER_FAILURE_MESSAGE, error=str(e))
        formatted_response = return_formatter(
            "failed",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            f"{COCKTAIL_REGISTER_FAILURE_MESSAGE}: {e!s}",
        )

    return ORJSONResponse(formatted_response, formatted_response["code"])


cocktail_maker.include_router(cocktail_maker_v1)

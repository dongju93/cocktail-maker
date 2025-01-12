from typing import Annotated, Any

import uvloop
from fastapi import Body, FastAPI, Path, Query, Request, Security
from fastapi.responses import ORJSONResponse

from auth import refresh_access_token, sign_in_token, verify_token
from database.query import (
    get_many_spirits_from_mongo,
    get_single_spirits_from_mongo,
    insert_spirits_to_mongo,
    user_sign_in,
    user_sign_up,
)
from model.response import SpiritsSearchResponse
from model.spirits import SpiritsRegister, SpiritsSearch
from model.user import Login, User

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
async def spirits_register(
    items: Annotated[list[SpiritsRegister], Body(...)],
) -> ORJSONResponse:
    inserted_object_id: str = await insert_spirits_to_mongo(items)
    return ORJSONResponse(content={"spirits_oid": inserted_object_id}, status_code=201)


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


@app.get("/version", summary="서비스 버전 확인")
async def version() -> ORJSONResponse:
    return ORJSONResponse(content={"version": version}, status_code=200)

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, Any
from uuid import uuid4

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from auth.roles import check_roles
from query.queries import Users
from utils.times import datetime_now, unix_to_datetime

load_dotenv(dotenv_path=".env")

# JWT 설정
SECRET_KEY: str = os.environ["SECRET_KEY"]
ALGORITHM: str = os.environ["SECRET_ALGORITHM"]
security = HTTPBearer()


@dataclass
class CreateToken:
    """
    Access, Refresh 토큰 생성 클래스
    """

    jti: str
    iat: datetime
    user_id: str

    def access(self, roles: list[str], expire_min: int = 500) -> str:
        """
        기본 15분 유효 기간의 액세스 토큰 생성 (테스트 500분)
        """
        token = {
            "sub": self.user_id,
            "jti": self.jti,
            "iat": self.iat,
            "exp": self.iat + timedelta(minutes=expire_min),
            "nbf": self.iat,
            "roles": roles,
            "iss": "cocktail-maker.co.kr/api",
            "aud": "cocktail-maker.co.kr",
            "type": "access",
        }
        return jwt.encode(token, SECRET_KEY, ALGORITHM)

    def refresh(self, expire_days: int = 7) -> str:
        """
        기본 7일 유효 기간의 리프레시 토큰 생성
        """
        token = {
            "sub": self.user_id,
            "jti": str(uuid4()),
            "iat": self.iat,
            "exp": self.iat + timedelta(days=expire_days),
            "nbf": self.iat,
            "iss": "cocktail-maker.co.kr/api",
            "aud": "cocktail-maker.co.kr",
            "type": "refresh",
            "access_jti": self.jti,
        }
        return jwt.encode(token, SECRET_KEY, ALGORITHM)


class PublishToken:
    @staticmethod
    def sign_in_token(user_id: str, roles: list[str]) -> dict[str, str]:
        """
        로그인 성공 시 JWT 반환
        """
        create_token = CreateToken(str(uuid4()), datetime_now(), user_id)
        access_payload: str = create_token.access(roles)
        refresh_payload: str = create_token.refresh()

        return {
            "accessToken": access_payload,
            "refreshToken": refresh_payload,
        }

    @staticmethod
    async def refresh_access_token(refresh_token: str) -> dict[str, str]:
        """
        리프레시 토큰을 받아 액세스 토큰을 갱신
        """
        try:
            refresh_payload = jwt.decode(
                refresh_token,
                SECRET_KEY,
                algorithms=ALGORITHM,
                audience="cocktail-maker.co.kr",
            )

            if refresh_payload["type"] != "refresh":
                raise InvalidTokenError("Invalid token type")

            create_token = CreateToken(
                refresh_payload["jti"], datetime_now(), refresh_payload["sub"]
            )

            # refresh 토큰에는 roles 정보가 없기 때문에 MongoDB 조회 후 access 토큰 생성 시 활용
            return {
                "accessToken": create_token.access(
                    await Users.get_roles(refresh_payload["sub"])
                )
            }

        except jwt.ExpiredSignatureError as ese:
            raise InvalidTokenError("Refresh token has expired") from ese
        except jwt.InvalidTokenError as ite:
            raise InvalidTokenError(f"Invalid refresh token: {ite!s}") from ite


class VerifyToken:
    def __call__(self, required_roles: list[str]):
        def verify(
            credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
        ):
            try:
                payload: dict[str, Any] = jwt.decode(
                    credentials.credentials,
                    SECRET_KEY,
                    ALGORITHM,
                    audience="cocktail-maker.co.kr",
                )

                # 시간 관련 변수 설정
                now: datetime = datetime_now()
                exp_time: datetime = unix_to_datetime(payload["exp"])
                nbf_time: datetime = unix_to_datetime(payload["nbf"])
                iat_time: datetime = unix_to_datetime(payload["iat"])

                # 시간 관련 검증
                if exp_time <= now:
                    raise InvalidTokenError("Token has expired")
                if nbf_time > now:
                    raise InvalidTokenError("Token is not yet valid")
                if iat_time > now:
                    raise InvalidTokenError("Token issued in the future")

                # 발행자 검증
                if payload["iss"] != "cocktail-maker.co.kr/api":
                    raise InvalidTokenError("Invalid issuer")

                # 토큰 타입 검증
                if payload["type"] != "access":
                    raise InvalidTokenError("Invalid token type")

                # 권한 검증
                if not check_roles(payload["roles"], required_roles):
                    raise HTTPException(
                        status_code=403, detail="Insufficient permissions"
                    )

            except jwt.ExpiredSignatureError as ese:
                raise HTTPException(
                    status_code=401, detail="Token has expired"
                ) from ese
            except jwt.InvalidAudienceError as iae:
                raise HTTPException(status_code=401, detail="Invalid audience") from iae
            except jwt.InvalidTokenError as ite:
                raise HTTPException(status_code=401, detail="Invalid token") from ite

        return verify

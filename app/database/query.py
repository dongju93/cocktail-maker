from base64 import urlsafe_b64decode
from datetime import UTC, datetime
from math import ceil
from typing import Any

from auth.encryption import Encryption
from fastapi import HTTPException
from model.response import SpiritsSearchResponse
from model.spirits import SpiritsRegister, SpiritsSearch
from model.user import Login, PasswordAndSalt, User
from pymongo.results import InsertManyResult

from database.connector import mongodb_conn
from database.query_assist import spirits_search_params


async def insert_spirits_to_mongo(items: list[SpiritsRegister]) -> str:
    try:
        all_data: list[dict[str, Any]] = []

        for item in items:
            data: dict[str, Any] = item.model_dump()
            # 생성 시간 추가
            data["created_at"] = datetime.now(tz=UTC)
            all_data.append(data)

        async with mongodb_conn("spirits") as conn:
            result: InsertManyResult = await conn.insert_many(all_data)
    except Exception as e:
        print("Insert Spirits object to mongodb raise an error")
        raise e

    return str(result.inserted_ids)


async def get_single_spirits_from_mongo(name: str) -> dict[str, Any]:
    try:
        async with mongodb_conn("spirits") as conn:
            result: dict[str, Any] | None = await conn.find_one({"name": name})
            if result is None:
                raise HTTPException(status_code=404, detail="Spirits not found")
    except Exception as e:
        print("Get Spirits object from mongodb raise an error")
        raise e
    else:
        result["_id"] = str(result["_id"])

    return result


async def get_many_spirits_from_mongo(params: SpiritsSearch) -> SpiritsSearchResponse:
    find_query: dict[str, dict[str, str]] = spirits_search_params(params)
    skip_count: int = (params.pageNumber - 1) * params.pageSize

    try:
        async with mongodb_conn("spirits") as conn:
            # 총 개수 조회
            total: int = await conn.count_documents(find_query)

            result: list[dict[str, Any]] = (
                await conn.find(find_query)
                .sort("name", 1)
                .skip(skip_count)
                .limit(params.pageSize)
                .to_list(10)
            )
    except Exception as e:
        print("Get Spirits object from mongodb raise an error")
        raise e
    else:
        for item in result:
            item["_id"] = str(item["_id"])

    return SpiritsSearchResponse(
        totalPage=ceil(total / params.pageSize),
        currentPage=params.pageNumber,
        totalSize=total,
        currentPageSize=len(result),
        items=result,
    )


async def user_sign_up(user: User) -> bool:
    encrypted_password_set: PasswordAndSalt = Encryption().passwords(user.password)

    try:
        data: dict[str, Any] = user.model_dump()
        # 비밀번호 암호화
        data["password"] = encrypted_password_set["encrypted_password"]
        # 솔트 추가
        data["salt"] = encrypted_password_set["salt"]
        # 생성 시간 추가
        data["created_at"] = datetime.now(tz=UTC)

        async with mongodb_conn("users") as conn:
            await conn.insert_one(data)
    except Exception:
        print("Insert User object to mongodb raise an error")
        return False

    return True


async def user_sign_in(login: Login) -> list[str]:
    try:
        async with mongodb_conn("users") as conn:
            result: dict[str, Any] | None = await conn.find_one(
                {"user_id": login.user_id}
            )
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")

            encrypted_password_set: PasswordAndSalt = Encryption().passwords(
                login.password, urlsafe_b64decode(result["salt"].encode())
            )

            if encrypted_password_set["encrypted_password"] != result["password"]:
                raise HTTPException(status_code=401, detail="Password is incorrect")
    except HTTPException:
        print("Get User object from mongodb raise an error")
        return []

    return result["roles"]


async def get_user_roles(user_id: str) -> list[str]:
    try:
        async with mongodb_conn("users") as conn:
            result: dict[str, Any] | None = await conn.find_one({"user_id": user_id})
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print("Get User object from mongodb raise an error")
        raise e

    return result["roles"]

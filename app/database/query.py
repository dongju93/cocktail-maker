from base64 import urlsafe_b64decode
from dataclasses import dataclass
from datetime import UTC, datetime
from math import ceil
from pathlib import Path
from sqlite3 import Cursor, Row
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from pymongo.results import InsertOneResult

from auth.encryption import Encryption
from database.connector import mongodb_conn, sqlite_conn
from database.query_assist import spirits_search_params
from model.response import SpiritsSearchResponse
from model.spirits import (
    SpiritsMetadataCategory,
    SpiritsMetadataRegister,
    SpiritsRegister,
    SpiritsSearch,
)
from model.user import Login, PasswordAndSalt, User
from utils.etc import save_image_to_local


@dataclass
class CreateSpirits:
    spirits_item: SpiritsRegister
    main_image: bytes
    sub_image1: bytes | None
    sub_image2: bytes | None
    sub_image3: bytes | None
    sub_image4: bytes | None

    async def save(self) -> str:
        try:
            async with mongodb_conn("spirits") as conn:
                result: InsertOneResult = await conn.insert_one(self.spirits_item)
        except Exception as e:
            print("Insert Spirits object to mongodb raise an error")
            raise e
        else:
            spirits_id: str = str(result.inserted_id)

        try:
            await self._image_saver(spirits_id)
        except Exception as e:
            print("Save Spirits images to local raise an error")
            raise e

        return spirits_id

    async def _image_saver(self, spirits_id: str) -> None:
        saved_image_paths: list[dict[str, str]] = []
        spirit_images: list[tuple[str, bytes | None]] = [
            ("main_image", self.main_image),
            ("sub_image_1", self.sub_image1),
            ("sub_image_2", self.sub_image2),
            ("sub_image_3", self.sub_image3),
            ("sub_image_4", self.sub_image4),
        ]

        # 이미지 저장 및 경로 정보 수집
        for image_key, image_data in spirit_images:
            if image_data is not None:
                image_path = Path(f"../data/images/{spirits_id}/{image_key}.png")
                save_image_to_local(image_data, image_path)
                saved_image_paths.append({"key": image_key, "path": str(image_path)})

        # 수집된 경로 정보를 SpiritsRegister에 대입
        for image_path_info in saved_image_paths:
            match image_path_info["key"]:
                case "main_image":
                    self.spirits_item["main_image"] = image_path_info["path"]
                case "sub_image_1":
                    self.spirits_item["sub_image_1"] = image_path_info["path"]
                case "sub_image_2":
                    self.spirits_item["sub_image_2"] = image_path_info["path"]
                case "sub_image_3":
                    self.spirits_item["sub_image_3"] = image_path_info["path"]
                case "sub_image_4":
                    self.spirits_item["sub_image_4"] = image_path_info["path"]

        await UpdateSpirits.save(spirits_id, self.spirits_item)


class ReadSpirits:
    @staticmethod
    async def based_on_name(name: str) -> dict[str, Any]:
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

    @staticmethod
    async def search(
        params: SpiritsSearch,
    ) -> SpiritsSearchResponse:
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


class UpdateSpirits:
    @staticmethod
    async def save(id: str, spirits_item: SpiritsRegister) -> None:
        spirits_item["updated_at"] = datetime.now(tz=UTC)
        async with mongodb_conn("spirits") as conn:
            await conn.update_one({"_id": ObjectId(id)}, {"$set": spirits_item})


class CreateSpiritsMetadata:
    @staticmethod
    def save(items: SpiritsMetadataRegister) -> bool:
        category: str = items.category
        names: list[str] = items.name
        try:
            with open("database/sql/insert_spirits_metadata.sql") as sql_file:
                sql: str = sql_file.read()

            with sqlite_conn() as conn:
                cursor: Cursor = conn.cursor()
                for name in names:
                    cursor.execute(
                        sql,
                        (category, name),
                    )
        except Exception:
            print("Insert Spirits metadata to sqlite raise an error")
            return False
        else:
            conn.commit()

        return True


class ReadSpiritsMetadata:
    @staticmethod
    def based_on_category(
        category: SpiritsMetadataCategory,
    ) -> list[dict[str, str]]:
        try:
            data: list[Row] = []
            result: list[dict[str, str]] = []
            with open("database/sql/get_spirits_metadata.sql") as sql_file:
                sql: str = sql_file.read()

            with sqlite_conn() as conn:
                cursor: Cursor = conn.cursor()
                cursor.execute(
                    sql,
                    (category.value,),
                )
                data = cursor.fetchall()
        except Exception as e:
            print("Get Spirits metadata from sqlite raise an error")
            raise e
        finally:
            if data != []:
                result = [{"id": row["id"], "name": row["name"]} for row in data]

        return result


class Users:
    @staticmethod
    async def sign_up(user: User) -> bool:
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

    @staticmethod
    async def sign_in(login: Login) -> list[str]:
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

    @staticmethod
    async def get_roles(user_id: str) -> list[str]:
        try:
            async with mongodb_conn("users") as conn:
                result: dict[str, Any] | None = await conn.find_one(
                    {"user_id": user_id}
                )
                if result is None:
                    raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            print("Get User object from mongodb raise an error")
            raise e

        return result["roles"]

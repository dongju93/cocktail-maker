from base64 import urlsafe_b64decode
from dataclasses import dataclass
from datetime import UTC, datetime
from math import ceil
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from pymongo.results import InsertOneResult
from sqlmodel import select
from structlog import BoundLogger

from auth.encryption import Encryption
from database.connector import mongodb_conn, sqlite_conn_orm
from database.query_assist import (
    Images,
    spirits_search_params,
)
from database.table import SpiritsMetadata
from model.response import SpiritsSearchResponse
from model.spirits import (
    SpiritsDict,
    SpiritsMetadataCategory,
    SpiritsMetadataRegister,
    SpiritsSearch,
)
from model.user import Login, PasswordAndSalt, User
from utils.logger import Logger

logger: BoundLogger = Logger().setup()


@dataclass
class CreateSpirits:
    spirits_item: SpiritsDict
    mainImage: bytes
    subImage1: bytes | None
    subImage2: bytes | None
    subImage3: bytes | None
    subImage4: bytes | None

    async def save(self) -> str:
        try:
            async with mongodb_conn("spirits") as conn:
                result: InsertOneResult = await conn.insert_one(self.spirits_item)
        except Exception as e:
            logger.error("Save Spirits object to mongodb has an error", error=str(e))
            raise e
        else:
            spirits_id: str = str(result.inserted_id)

        try:
            await Images().save_image_files_to_local_dir(
                spirits_id,
                self.mainImage,
                self.subImage1,
                self.subImage2,
                self.subImage3,
                self.subImage4,
            )
        except Exception as e:
            logger.error("Save Spirits images to local has an error", error=str(e))
            raise e

        return spirits_id


class ReadSpirits:
    @staticmethod
    async def based_on_name(name: str) -> dict[str, Any]:
        try:
            async with mongodb_conn("spirits") as conn:
                result: dict[str, Any] | None = await conn.find_one({"name": name})
                if result is None:
                    raise HTTPException(status_code=404, detail="Spirits not found")
        except Exception as e:
            logger.error(
                "Get single Spirits object from mongodb has an error", error=str(e)
            )
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
            logger.error(
                "Search Spirits objects from mongodb has an error", error=str(e)
            )
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


@dataclass
class UpdateSpirits:
    document_id: str
    spirits_item: SpiritsDict
    main_image: bytes
    sub_image1: bytes | None
    sub_image2: bytes | None
    sub_image3: bytes | None
    sub_image4: bytes | None

    async def update(self) -> None:
        # 1. 기존 이미지 삭제
        await Images().remove_image_files_in_local_dir(self.document_id)

        # 2. 문서 업데이트
        try:
            async with mongodb_conn("spirits") as conn:
                self.spirits_item["updated_at"] = datetime.now(tz=UTC)
                result = await conn.update_one(
                    {"_id": ObjectId(self.document_id)}, {"$set": self.spirits_item}
                )
                if result.matched_count == 0:
                    raise HTTPException(status_code=404, detail="Spirits not found")
        except Exception as e:
            logger.error("Update Spirits object has an error", error=str(e))
            raise e

        # 3. 새 이미지 저장
        try:
            await Images().save_image_files_to_local_dir(
                self.document_id,
                self.main_image,
                self.sub_image1,
                self.sub_image2,
                self.sub_image3,
                self.sub_image4,
            )
        except Exception as e:
            logger.error("Save updated Spirits images has an error", error=str(e))
            raise e


@dataclass
class DeleteSpirits:
    id: str

    async def remove(self) -> None:
        try:
            await Images().remove_image_files_in_local_dir(self.id)

            async with mongodb_conn("spirits") as conn:
                result = await conn.delete_one({"_id": ObjectId(self.id)})
                if result.deleted_count == 0:
                    raise HTTPException(404, "Spirits not found")
        except Exception as e:
            logger.error(
                "Delete Spirits object from mongodb has an error", error=str(e)
            )
            raise e


class CreateSpiritsMetadata:
    @staticmethod
    def save(category: SpiritsMetadataCategory, items: SpiritsMetadataRegister) -> None:
        try:
            with sqlite_conn_orm() as session:
                for name in items.name:
                    metadata = SpiritsMetadata(category=category.value, name=name)  # type: ignore
                    session.add(metadata)
                session.commit()
        except Exception as e:
            logger.error("Insert Spirits metadata to sqlite has an error", error=str(e))
            raise e


class ReadSpiritsMetadata:
    @staticmethod
    def based_on_category(
        category: SpiritsMetadataCategory,
    ) -> list[dict[str, int | str]]:
        try:
            with sqlite_conn_orm() as session:
                statement = (
                    select(SpiritsMetadata.id, SpiritsMetadata.name)
                    .where(SpiritsMetadata.category == category.value)
                    .order_by(SpiritsMetadata.name)
                )

        except Exception as e:
            logger.error("Get Spirits metadata from sqlite has an error", error=str(e))
            raise e

        return [{"index": id, "name": name} for id, name in session.exec(statement)]


class DeleteSpiritsMetadata:
    @staticmethod
    def remove(metadata_id: int) -> None:
        try:
            with sqlite_conn_orm() as session:
                metadata: SpiritsMetadata | None = session.get(
                    SpiritsMetadata, metadata_id
                )
                if metadata is None:
                    raise HTTPException(404, "Metadata not found")

                session.delete(metadata)
                session.commit()
        except Exception as e:
            logger.error("Delete Spirits metadata has an error", error=str(e))
            raise e


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
        except Exception as e:
            logger.error(
                "Insert User credentials to mongodb has an error", error=str(e)
            )
            return False

        return True

    @staticmethod
    async def sign_in(login: Login) -> list[str]:
        try:
            async with mongodb_conn("users") as conn:
                result: dict[str, Any] | None = await conn.find_one(
                    {"user_id": login.userId}
                )
                if result is None:
                    raise HTTPException(status_code=404, detail="User not found")

                encrypted_password_set: PasswordAndSalt = Encryption().passwords(
                    login.password, urlsafe_b64decode(result["salt"].encode())
                )

                if encrypted_password_set["encrypted_password"] != result["password"]:
                    raise HTTPException(status_code=401, detail="Password is incorrect")
        except HTTPException as he:
            logger.error(
                "Get User credentials from mongodb has an error",
                code=he.status_code,
                message=he.detail,
            )
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
            logger.error("Get User roles from mongodb has an error", error=str(e))
            raise e

        return result["roles"]

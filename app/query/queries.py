from base64 import urlsafe_b64decode
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from sqlmodel import and_, select
from structlog import BoundLogger

from auth import Encryption
from database import MetadataTable, mongodb_conn, sqlite_conn_orm
from model import (
    METADATA_KIND,
    LiqueurDict,
    LiqueurSearch,
    Login,
    MetadataCategory,
    MetadataRegister,
    PasswordAndSalt,
    SearchResponse,
    SpiritsDict,
    SpiritsSearch,
    User,
)
from utils import Logger

from .query_child import Images, liqueur_search_query, spirits_search_query
from .query_parents import CreateDocument, RetrieveDocument, SearchDocument

logger: BoundLogger = Logger().setup()


@dataclass
class CreateSpirits(CreateDocument):
    spirits_item: SpiritsDict
    mainImage: bytes
    subImage1: bytes | None
    subImage2: bytes | None
    subImage3: bytes | None
    subImage4: bytes | None

    async def save(self) -> str:
        document_id: str = await super().save()

        try:
            await Images().save_image_files_to_local_dir(
                document_id, "liqueur", self.mainImage
            )
        except Exception as e:
            logger.error(
                f"Save liqueur images to local has an error: {str(object=e)}",
            )
            raise e

        return document_id

    def get_collection_name(self) -> str:
        return "spirits"

    def get_document(self) -> SpiritsDict:
        return self.spirits_item


@dataclass
class CreateLiqueur(CreateDocument):
    liqueur_item: LiqueurDict
    mainImage: bytes
    collection_name: str = "liqueur"

    async def save(self) -> str:
        document_id: str = await super().save()

        try:
            await Images().save_image_files_to_local_dir(
                document_id, "liqueur", self.mainImage
            )
        except Exception as e:
            logger.error(
                f"Save liqueur images to local has an error: {str(object=e)}",
            )
            raise e

        return document_id

    def get_collection_name(self) -> str:
        return self.collection_name

    def get_document(self) -> LiqueurDict:
        return self.liqueur_item


@dataclass
class RetrieveSpirits(RetrieveDocument):
    name: str
    collection_name: str = "spirits"

    async def only_name(self) -> dict[str, Any]:
        document: dict[str, Any] = await super().only_name()

        return document

    def get_collection_name(self) -> str:
        return self.collection_name

    def get_name(self) -> str:
        return self.name


@dataclass
class SearchSpirits(SearchDocument):
    params: SpiritsSearch
    collection_name: str = "spirits"

    async def query(self) -> SearchResponse:
        documents: SearchResponse = await super().query()

        return documents

    def get_collection_name(self) -> str:
        return self.collection_name

    def get_query(self) -> dict[str, Any]:
        return spirits_search_query(self.params)

    def get_params(self) -> SpiritsSearch:
        return self.params


@dataclass
class RetrieveLiqueur(RetrieveDocument):
    name: str
    collection_name: str = "liqueur"

    async def only_name(self) -> dict[str, Any]:
        document: dict[str, Any] = await super().only_name()

        return document

    def get_collection_name(self) -> str:
        return self.collection_name

    def get_name(self) -> str:
        return self.name


@dataclass
class SearchLiqueur(SearchDocument):
    params: LiqueurSearch
    collection_name: str = "liqueur"

    async def query(self) -> SearchResponse:
        documents: SearchResponse = await super().query()

        return documents

    def get_collection_name(self) -> str:
        return self.collection_name

    def get_query(self) -> dict[str, Any]:
        return liqueur_search_query(self.params)

    def get_params(self) -> LiqueurSearch:
        return self.params


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
                "spirits",
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


class Metadata:
    @staticmethod
    def create(
        category: MetadataCategory,
        items: MetadataRegister,
        kind: METADATA_KIND,
    ) -> None:
        try:
            with sqlite_conn_orm() as session:
                for name in items.names:
                    metadata = MetadataTable(
                        category=category.value, name=name, kind=kind
                    )  # type: ignore
                    session.add(metadata)
                session.commit()
        except Exception as e:
            logger.error("Insert Spirits metadata to sqlite has an error", error=str(e))
            raise e

    @staticmethod
    def read(
        category: MetadataCategory,
        kind: METADATA_KIND,
    ) -> list[dict[str, int | str]]:
        try:
            with sqlite_conn_orm() as session:
                statement = (
                    select(MetadataTable.id, MetadataTable.name)
                    .where(
                        and_(
                            MetadataTable.category == category.value,
                            MetadataTable.kind == kind,
                        )
                    )
                    .order_by(MetadataTable.name)
                )

        except Exception as e:
            logger.error("Get Spirits metadata from sqlite has an error", error=str(e))
            raise e

        return [{"index": id, "name": name} for id, name in session.exec(statement)]

    @staticmethod
    def delete(metadata_id: int) -> None:
        try:
            with sqlite_conn_orm() as session:
                metadata: MetadataTable | None = session.get(MetadataTable, metadata_id)
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

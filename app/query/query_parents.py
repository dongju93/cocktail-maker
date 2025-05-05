from abc import ABC, abstractmethod
from math import ceil
from typing import Any

from fastapi import HTTPException
from pymongo.results import InsertOneResult
from structlog import BoundLogger

from database.connector import mongodb_conn
from model.liqueur import LiqueurDict, LiqueurSearch
from model.response import SearchResponse
from model.spirits import (
    SpiritsDict,
    SpiritsSearch,
)
from utils.logger import Logger

logger: BoundLogger = Logger().setup()


class CreateDocument(ABC):
    async def save(self) -> str:
        collection_name: str = ""

        try:
            collection_name: str = self.get_collection_name()
            document: SpiritsDict | LiqueurDict = self.get_document()

            async with mongodb_conn(collection_name) as conn:
                result: InsertOneResult = await conn.insert_one(document)
        except Exception as e:
            logger.error(
                f"Save {collection_name} object to mongodb has an error",
                error=str(e),
            )
            raise e
        else:
            document_id: str = str(result.inserted_id)

        return document_id

    @abstractmethod
    def get_collection_name(self) -> str:
        """컬랙션 이름"""
        pass

    @abstractmethod
    def get_document(self) -> SpiritsDict | LiqueurDict:
        """문서, TypedDict"""
        pass


class RetrieveDocument(ABC):
    async def only_name(self) -> dict[str, Any]:
        collection_name: str = self.get_collection_name()
        name: str = self.get_name()

        try:
            collection_name: str = self.get_collection_name()
            async with mongodb_conn(collection_name) as conn:
                result: dict[str, Any] | None = await conn.find_one({"name": name})
                if result is None:
                    raise HTTPException(
                        status_code=404, detail=f"{collection_name} not found"
                    )
        except Exception as e:
            logger.error(
                f"Get single {collection_name} object from mongodb has an error",
                error=str(e),
            )
            raise e
        else:
            result["_id"] = str(result["_id"])

        return result

    @abstractmethod
    def get_collection_name(self) -> str:
        """컬랙션 이름"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """문서 이름"""
        pass


class SearchDocument(ABC):
    async def query(
        self,
    ) -> SearchResponse:
        collection_name: str = ""
        find_query: dict[str, Any] = {}
        total: int = 0
        result: list[dict[str, Any]] = []

        collection_name = self.get_collection_name()
        find_query: dict[str, Any] = self.get_query()
        params: SpiritsSearch | LiqueurSearch = self.get_params()

        skip_count: int = (params.pageNumber - 1) * params.pageSize

        try:
            async with mongodb_conn(collection_name) as conn:
                # 총 개수 조회
                total = await conn.count_documents(find_query)

                result = (
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

        return SearchResponse(
            totalPage=ceil(total / params.pageSize),
            currentPage=params.pageNumber,
            totalSize=total,
            currentPageSize=len(result),
            items=result,
        )

    @abstractmethod
    def get_collection_name(self) -> str:
        """컬랙션 이름"""
        pass

    @abstractmethod
    def get_query(self) -> dict[str, Any]:
        """검색 쿼리"""
        pass

    @abstractmethod
    def get_params(self) -> Any:
        """검색 파라미터"""
        pass

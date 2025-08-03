from datetime import UTC, datetime
from pathlib import Path
from shutil import rmtree
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from structlog import BoundLogger

from database import mongodb_conn
from model import (
    COCKTAIL_DATA_KIND,
    IngredientSearch,
    LiqueurSearchQuery,
    SpiritsSearch,
)
from utils import Logger, save_image_to_local

logger: BoundLogger = Logger().setup()


def spirits_search_query(params: SpiritsSearch) -> dict[str, Any]:
    """
    SpiritsSearch 클래스의 모든 필드를 MongoDB 쿼리로 변환합니다.

    Args:
        params: 검색 파라미터

    Returns:
        MongoDB 쿼리 딕셔너리
    """
    query: dict[str, Any] = {}

    # 이름 검색 (부분 일치)
    if params.name is not None:
        query["name"] = {"$regex": params.name, "$options": "i"}  # 대소문자 무시 옵션

    # 향 검색 (목록 중 정확한 일치)
    if params.aroma is not None and len(params.aroma) > 0:
        query["aroma"] = {"$all": params.aroma}

    # 맛 검색 (목록 중 정확한 일치)
    if params.taste is not None and len(params.taste) > 0:
        query["taste"] = {"$all": params.taste}

    # 여운 검색 (목록 중 정확한 일치)
    if params.finish is not None and len(params.finish) > 0:
        query["finish"] = {"$all": params.finish}

    # 종류 검색 (정확한 일치)
    if params.kind is not None:
        query["kind"] = params.kind

    # 세부 종류 검색 (정확한 일치)
    if params.sub_kind is not None:
        query["sub_kind"] = params.sub_kind

    # 알코올 도수 범위 검색
    alcohol_query: dict[str, float] = {}
    if params.min_alcohol is not None:
        alcohol_query["$gte"] = params.min_alcohol
    if params.max_alcohol is not None:
        alcohol_query["$lte"] = params.max_alcohol
    if alcohol_query:
        query["alcohol"] = alcohol_query

    # 원산지 국가 검색 (정확한 일치)
    if params.origin_nation is not None:
        query["origin_nation"] = params.origin_nation

    # 원산지 지역 검색 (부분 일치)
    if params.origin_location is not None:
        query["origin_location"] = {"$regex": params.origin_location, "$options": "i"}

    return query


def liqueur_search_query(params: LiqueurSearchQuery) -> dict[str, Any]:
    """
    LiqueurSearchQuery 클래스의 모든 필드를 MongoDB 쿼리로 변환합니다.

    Args:
        params: 검색 파라미터

    Returns:
        MongoDB 쿼리 딕셔너리
    """
    query: dict[str, Any] = {}

    # 이름 검색 (부분 일치)
    if params.name is not None:
        query["name"] = {"$regex": params.name, "$options": "i"}  # 대소문자 무시 옵션

    # 브랜드 검색 (정확한 일치)
    if params.brand is not None:
        query["brand"] = params.brand

    # 맛 검색 (목록 중 정확한 일치)
    if params.taste is not None and len(params.taste) > 0:
        query["taste"] = {"$all": params.taste}

    # 종류 검색 (정확한 일치)
    if params.kind is not None:
        query["kind"] = params.kind

    # 세부 종류 검색 (정확한 일치)
    if params.sub_kind is not None:
        query["sub_kind"] = params.sub_kind

    # 주재료 검색 (목록 중 정확한 일치)
    if params.main_ingredients is not None and len(params.main_ingredients) > 0:
        query["main_ingredients"] = {"$all": params.main_ingredients}

    # 용량 범위 검색
    volume_query: dict[str, float] = {}
    if params.min_volume is not None:
        volume_query["$gte"] = params.min_volume
    if params.max_volume is not None:
        volume_query["$lte"] = params.max_volume
    if volume_query:
        query["volume"] = volume_query

    # 알코올 도수 범위 검색
    abv_query: dict[str, float] = {}
    if params.min_abv is not None:
        abv_query["$gte"] = params.min_abv
    if params.max_abv is not None:
        abv_query["$lte"] = params.max_abv
    if abv_query:
        query["abv"] = abv_query

    # 원산지 국가 검색 (정확한 일치)
    if params.origin_nation is not None:
        query["origin_nation"] = params.origin_nation

    # 원산지 지역 검색 (부분 일치)
    if params.origin_location is not None:
        query["origin_location"] = {"$regex": params.origin_location, "$options": "i"}

    # 설명 검색 (부분 일치)
    if params.description is not None:
        query["description"] = {"$regex": params.description, "$options": "i"}

    return query


def ingredient_search_query(params: IngredientSearch) -> dict[str, Any]:
    """
    IngredientSearch 클래스의 모든 필드를 MongoDB 쿼리로 변환합니다.

    Args:
        params: 검색 파라미터

    Returns:
        MongoDB 쿼리 딕셔너리
    """
    query: dict[str, Any] = {}

    # 이름 검색 (부분 일치)
    if params.name is not None:
        query["name"] = {"$regex": params.name, "$options": "i"}  # 대소문자 무시 옵션

    # 브랜드 검색 (목록 중 정확한 일치)
    if params.brand is not None and len(params.brand) > 0:
        query["brand"] = {"$all": params.brand}

    # 종류 검색 (정확한 일치)
    if params.kind is not None:
        query["kind"] = params.kind

    # 설명 검색 (부분 일치)
    if params.description is not None:
        query["description"] = {"$regex": params.description, "$options": "i"}

    return query


class Images:
    @classmethod
    async def remove_image_files_in_local_dir(cls, id: str) -> None:
        """이미지 파일 삭제"""
        try:
            async with mongodb_conn("spirits") as conn:
                result: dict[str, Any] | None = await conn.find_one(
                    {"_id": ObjectId(id)}
                )
                if result is None:
                    raise HTTPException(404, "Spirits not found")
        except Exception as e:
            logger.error("Get Spirits object from mongodb has an error", error=str(e))
            raise e
        else:
            rmtree(Path(result["main_image"]).parent, ignore_errors=True)

    @classmethod
    async def _image_field_updater(
        cls, collection_name: COCKTAIL_DATA_KIND, id: str, image_data: dict[str, Any]
    ) -> None:
        image_data["updated_at"] = datetime.now(tz=UTC)
        async with mongodb_conn(collection_name) as conn:
            await conn.update_one({"_id": ObjectId(id)}, {"$set": image_data})

    @classmethod
    async def save_image_files_to_local_dir(  # noqa: PLR0913
        cls,
        document_id: str,
        collection_name: COCKTAIL_DATA_KIND,
        main_image: bytes | None = None,
        sub_image1: bytes | None = None,
        sub_image2: bytes | None = None,
        sub_image3: bytes | None = None,
        sub_image4: bytes | None = None,
    ) -> None:
        saved_image_paths: list[dict[str, str]] = []
        spirit_images: list[tuple[str, bytes | None]] = [
            ("main_image", main_image),
            ("sub_image_1", sub_image1),
            ("sub_image_2", sub_image2),
            ("sub_image_3", sub_image3),
            ("sub_image_4", sub_image4),
        ]

        # 이미지 저장 및 경로 정보 수집
        for image_key, image_data in spirit_images:
            if image_data is not None:
                image_path = Path(
                    f"../data/images/{collection_name}/{document_id}/{image_key}.png"
                )
                save_image_to_local(image_data, image_path)
                saved_image_paths.append({"key": image_key, "path": str(image_path)})

        update_image: dict[str, Any] = {}
        # 수집된 경로 정보를 Dict에 추가
        for image_path_info in saved_image_paths:
            # main_image, sub_image_1, sub_image_2, sub_image_3, sub_image_4 필드 처리
            update_image[image_path_info["key"]] = image_path_info["path"]

        await cls._image_field_updater(collection_name, document_id, update_image)

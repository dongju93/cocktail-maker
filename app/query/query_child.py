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
    CocktailSearchQuery,
    IngredientSearch,
    LiqueurSearchQuery,
    SpiritsSearch,
)
from utils import Logger, save_image_to_local

logger: BoundLogger = Logger().setup()


def _set_regex_query(query: dict[str, Any], field_name: str, value: str | None) -> None:
    if value is not None:
        query[field_name] = {"$regex": value, "$options": "i"}


def _set_exact_query(query: dict[str, Any], field_name: str, value: str | None) -> None:
    if value is not None:
        query[field_name] = value


def _set_all_query(
    query: dict[str, Any], field_name: str, value: list[str] | None
) -> None:
    if value is not None and len(value) > 0:
        query[field_name] = {"$all": value}


def _set_range_query(
    query: dict[str, Any],
    field_name: str,
    min_value: float | None,
    max_value: float | None,
) -> None:
    range_query: dict[str, float] = {}

    if min_value is not None:
        range_query["$gte"] = min_value
    if max_value is not None:
        range_query["$lte"] = max_value
    if range_query:
        query[field_name] = range_query


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

    _set_regex_query(query, "name", params.name)
    _set_all_query(query, "taste", params.taste)
    _set_all_query(query, "main_ingredients", params.main_ingredients)
    _set_range_query(query, "volume", params.min_volume, params.max_volume)
    _set_range_query(query, "abv", params.min_abv, params.max_abv)
    _set_regex_query(query, "origin_location", params.origin_location)
    _set_regex_query(query, "description", params.description)

    for field_name in ("brand", "kind", "sub_kind", "origin_nation"):
        _set_exact_query(query, field_name, getattr(params, field_name))

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


def cocktail_search_query(params: CocktailSearchQuery) -> dict[str, Any]:
    """Convert cocktail search parameters to a MongoDB query."""

    query: dict[str, Any] = {}

    if params.name is not None:
        query["name"] = {"$regex": params.name, "$options": "i"}

    if params.aroma is not None and len(params.aroma) > 0:
        query["aroma"] = {"$all": params.aroma}

    if params.taste is not None and len(params.taste) > 0:
        query["taste"] = {"$all": params.taste}

    if params.finish is not None and len(params.finish) > 0:
        query["finish"] = {"$all": params.finish}

    if params.glass is not None:
        query["glass"] = params.glass

    if params.origin_nation is not None:
        query["origin_nation"] = params.origin_nation

    if params.description is not None:
        query["description"] = {"$regex": params.description, "$options": "i"}

    if params.ingredient_ids is not None and len(params.ingredient_ids) > 0:
        query["ingredients.id"] = {"$all": params.ingredient_ids}

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

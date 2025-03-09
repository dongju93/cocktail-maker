from typing import Any

from model.spirits import SpiritsSearch


def spirits_search_params(params: SpiritsSearch) -> dict[str, Any]:
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
    if params.subKind is not None:
        query["subKind"] = params.subKind

    # 알코올 도수 범위 검색
    alcohol_query: dict[str, float] = {}
    if params.alcohol_min is not None:
        alcohol_query["$gte"] = params.alcohol_min
    if params.alcohol_max is not None:
        alcohol_query["$lte"] = params.alcohol_max
    if alcohol_query:
        query["alcohol"] = alcohol_query

    # 원산지 국가 검색 (정확한 일치)
    if params.origin_nation is not None:
        query["origin_nation"] = params.origin_nation

    # 원산지 지역 검색 (부분 일치)
    if params.origin_location is not None:
        query["origin_location"] = {"$regex": params.origin_location, "$options": "i"}

    return query

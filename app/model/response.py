from typing import Any, Literal, TypedDict


class SearchResponse(TypedDict):
    """
    총 검색 개수, 총 페이지 수, 현재 페이지 개수,
    현재 페이지 번호, 검색 결과 목록 응답 구조
    """

    totalPage: int
    currentPage: int
    totalSize: int
    currentPageSize: int
    items: list[dict[str, Any]]


class ResponseFormat(TypedDict):
    status: Literal["success", "failed"]
    code: int
    data: Any
    message: str

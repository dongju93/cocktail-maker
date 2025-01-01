from typing import Any

from app.model.spirits import SpiritsSearch


def spirits_search_params(
    params: SpiritsSearch,
) -> dict[str, Any]:
    find_query: dict = {}

    if params.name is not None:
        find_query["name"] = {"$regex": f".*{params.name}.*", "$options": "i"}

    if params.aroma is not None:
        find_query["aroma"] = {"$in": params.aroma}

    return find_query

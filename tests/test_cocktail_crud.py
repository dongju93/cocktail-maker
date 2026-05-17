from unittest.mock import AsyncMock, patch

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from httpx import Response

from conftest import api_service

client = TestClient(api_service, base_url="http://localhost")


def _cocktail_payload() -> dict[str, object]:
    return {
        "name": "네그로니",
        "aroma": ["시트러스"],
        "taste": ["쓴맛"],
        "finish": ["드라이"],
        "ingredients": [
            {
                "id": "507f1f77bcf86cd799439011",
                "type": "liquor",
                "amount": 30,
                "unit": "ml",
            },
            {
                "id": "507f1f77bcf86cd799439012",
                "type": "spirits",
                "amount": 30,
                "unit": "ml",
            },
        ],
        "steps": [
            {"step": 1, "description": "재료를 넣고 섞는다."},
            {"step": 2, "description": "잔에 따른다."},
        ],
        "glass": "올드 패션드",
        "description": "쓴맛과 향이 선명한 클래식 칵테일",
        "origin_nation": "이탈리아",
    }


def test_cocktail_detail_success() -> None:
    cocktail = {
        "_id": "507f1f77bcf86cd799439099",
        "name": "네그로니",
        "glass": "올드 패션드",
    }

    with patch("query.queries.RetrieveCocktail") as mock_retrieve:
        mock_instance = AsyncMock()
        mock_retrieve.return_value = mock_instance
        mock_instance.only_name.return_value = cocktail

        response: Response = client.get("/api/v1/cocktails/네그로니")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "success",
            "code": 200,
            "data": cocktail,
            "message": "Successfully get cocktail",
        }
        mock_retrieve.assert_called_once_with("네그로니")
        mock_instance.only_name.assert_awaited_once()


def test_cocktail_search_success() -> None:
    search_result = {
        "totalPage": 1,
        "currentPage": 1,
        "totalSize": 1,
        "currentPageSize": 1,
        "items": [{"_id": "507f1f77bcf86cd799439099", "name": "네그로니"}],
    }

    with patch("query.queries.SearchCocktail") as mock_search:
        mock_instance = AsyncMock()
        mock_search.return_value = mock_instance
        mock_instance.query.return_value = search_result

        response: Response = client.get(
            "/api/v1/cocktails",
            params={"name": "네그", "pageNumber": 1, "pageSize": 10},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "success",
            "code": 200,
            "data": search_result,
            "message": "Successfully search cocktails",
        }
        mock_search.assert_called_once()
        mock_instance.query.assert_awaited_once()


def test_cocktail_update_success_normalizes_recipe_type() -> None:
    document_id = "507f1f77bcf86cd799439011"
    payload = _cocktail_payload()

    with (
        patch("query.metadata.MetadataValidation") as mock_validation,
        patch("query.queries.UpdateCocktail") as mock_update,
    ):
        mock_validation.return_value.return_value = (
            payload["taste"],
            payload["aroma"],
            payload["finish"],
        )
        mock_instance = AsyncMock()
        mock_update.return_value = mock_instance
        mock_instance.update.return_value = None

        response: Response = client.put(
            f"/api/v1/cocktails/{document_id}",
            json=payload,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_update.assert_called_once()
        called_document_id, called_item = mock_update.call_args.args
        assert called_document_id == document_id
        assert called_item["ingredients"][0]["type"] == "liqueur"
        mock_instance.update.assert_awaited_once()


def test_cocktail_delete_success() -> None:
    document_id = "507f1f77bcf86cd799439011"

    with patch("query.queries.DeleteCocktail") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.return_value = None

        response: Response = client.delete(f"/api/v1/cocktails/{document_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "success",
            "code": 200,
            "data": None,
            "message": "Successfully delete cocktail",
        }
        mock_delete.assert_called_once_with(document_id)
        mock_instance.remove.assert_awaited_once()


def test_cocktail_delete_not_found() -> None:
    document_id = "507f1f77bcf86cd799439011"

    with patch("query.queries.DeleteCocktail") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.side_effect = HTTPException(
            status_code=404, detail="Cocktail not found"
        )

        response: Response = client.delete(f"/api/v1/cocktails/{document_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "status": "failed",
            "code": 404,
            "data": None,
            "message": "Cocktail not found",
        }


def test_cocktail_update_invalid_document_id_length() -> None:
    response: Response = client.put(
        "/api/v1/cocktails/short-id", json=_cocktail_payload()
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

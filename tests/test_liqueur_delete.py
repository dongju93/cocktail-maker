import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from conftest import api_service

client = TestClient(api_service)


def test_liqueur_delete_success() -> None:
    """Test successful liqueur deletion"""
    document_id = "507f1f77bcf86cd799439011"  # Valid MongoDB ObjectId format
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.return_value = None
        
        response: Response = client.delete(f"/api/v1/liqueur/{document_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "success",
            "code": 200,
            "data": None,
            "message": "Successfully delete liqueur",
        }
        
        # Verify that DeleteLiqueur was called with correct parameters
        mock_delete.assert_called_once_with(document_id)
        mock_instance.remove.assert_called_once()


def test_liqueur_delete_invalid_document_id_length() -> None:
    """Test liqueur deletion with invalid document_id length"""
    # Test with too short document_id
    short_id = "507f1f77bcf"
    response: Response = client.delete(f"/api/v1/liqueur/{short_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test with too long document_id
    long_id = "507f1f77bcf86cd799439011abc"
    response = client.delete(f"/api/v1/liqueur/{long_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_liqueur_delete_not_found() -> None:
    """Test liqueur deletion when liqueur is not found"""
    document_id = "507f1f77bcf86cd799439011"
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        from fastapi import HTTPException
        
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.side_effect = HTTPException(
            status_code=404, detail="Liqueur not found"
        )
        
        response: Response = client.delete(f"/api/v1/liqueur/{document_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "status": "failed",
            "code": 404,
            "data": None,
            "message": "Liqueur not found",
        }


def test_liqueur_delete_internal_server_error() -> None:
    """Test liqueur deletion with internal server error"""
    document_id = "507f1f77bcf86cd799439011"
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.side_effect = Exception("Database connection error")
        
        response: Response = client.delete(f"/api/v1/liqueur/{document_id}")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {
            "status": "failed",
            "code": 500,
            "data": None,
            "message": "Failed to delete liqueur: Database connection error",
        }


def test_liqueur_delete_method_not_allowed() -> None:
    """Test liqueur deletion endpoint with wrong HTTP method"""
    document_id = "507f1f77bcf86cd799439011"
    
    # Test POST method on delete endpoint
    response: Response = client.post(f"/api/v1/liqueur/{document_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_liqueur_delete_async_success() -> None:
    """Test successful liqueur deletion in async mode"""
    document_id = "507f1f77bcf86cd799439011"
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.return_value = None
        
        response = await asyncio.to_thread(
            client.delete, f"/api/v1/liqueur/{document_id}"
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "success"
        assert response.json()["message"] == "Successfully delete liqueur"


@pytest.mark.asyncio
async def test_liqueur_delete_multiple_concurrent_requests() -> None:
    """Test multiple concurrent liqueur deletion requests"""
    document_ids = [
        "507f1f77bcf86cd799439011",
        "507f1f77bcf86cd799439012", 
        "507f1f77bcf86cd799439013"
    ]
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.return_value = None
        
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    asyncio.to_thread(client.delete, f"/api/v1/liqueur/{doc_id}")
                )
                for doc_id in document_ids
            ]
        
        # Verify all requests succeeded
        responses = [task.result() for task in tasks]
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "success"
        
        # Verify DeleteLiqueur was called for each document_id
        assert mock_delete.call_count == len(document_ids)


@pytest.mark.asyncio
async def test_liqueur_delete_mixed_success_failure() -> None:
    """Test mixed success and failure scenarios for liqueur deletion"""
    valid_id = "507f1f77bcf86cd799439011" 
    not_found_id = "507f1f77bcf86cd799439012"
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        def mock_delete_side_effect(document_id: str):
            mock_instance = AsyncMock()
            if document_id == not_found_id:
                from fastapi import HTTPException
                mock_instance.remove.side_effect = HTTPException(
                    status_code=404, detail="Liqueur not found"
                )
            else:
                mock_instance.remove.return_value = None
            return mock_instance
        
        mock_delete.side_effect = mock_delete_side_effect
        
        async with asyncio.TaskGroup() as tg:
            success_task = tg.create_task(
                asyncio.to_thread(client.delete, f"/api/v1/liqueur/{valid_id}")
            )
            failure_task = tg.create_task(
                asyncio.to_thread(client.delete, f"/api/v1/liqueur/{not_found_id}")
            )
        
        success_response = success_task.result()
        failure_response = failure_task.result()
        
        assert success_response.status_code == status.HTTP_200_OK
        assert success_response.json()["status"] == "success"
        
        assert failure_response.status_code == status.HTTP_404_NOT_FOUND
        assert failure_response.json()["status"] == "failed"


def test_liqueur_delete_response_headers() -> None:
    """Test liqueur deletion response headers"""
    document_id = "507f1f77bcf86cd799439011"
    
    with patch("query.queries.DeleteLiqueur") as mock_delete:
        mock_instance = AsyncMock()
        mock_delete.return_value = mock_instance
        mock_instance.remove.return_value = None
        
        response: Response = client.delete(f"/api/v1/liqueur/{document_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"
        # Check for custom headers if any
        assert "X-Server-Version" in response.headers


def test_liqueur_delete_invalid_endpoint() -> None:
    """Test invalid liqueur deletion endpoints"""
    # Test with missing document_id - this should return 405 because
    # /api/v1/liqueur/ is a valid endpoint but DELETE is not allowed
    response: Response = client.delete("/api/v1/liqueur/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    # Test with invalid path
    response = client.delete("/api/v1/liqueur/delete/invalid")
    assert response.status_code == status.HTTP_404_NOT_FOUND
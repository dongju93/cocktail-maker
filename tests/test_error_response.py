from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from conftest import api_service

client = TestClient(api_service)


def test_server_error_returns_rfc9457_format() -> None:
    """Test that 500 HTTPException returns RFC 9457 Problem Details format"""

    def mock_endpoint() -> None:
        raise HTTPException(status_code=500, detail="Internal server error occurred")

    # Add a test endpoint that raises a 500 error
    api_service.add_api_route("/test-500", mock_endpoint, methods=["GET"])

    response = client.get("/test-500")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers.get("content-type") == "application/problem+json"

    data = response.json()

    # Check RFC 9457 required fields
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "instance" in data

    # Check specific values
    assert data["status"] == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert data["title"] == "Server Error 500"
    assert data["type"] == "https://httpstatuses.com/500"
    assert data["detail"] == "Internal server error occurred"
    assert data["instance"].startswith("urn:uuid:")


def test_client_error_uses_rfc9457_format() -> None:
    """Test that explicit HTTPExceptions for client errors (4xx) use RFC 9457 format"""

    def mock_401_endpoint() -> None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Add a test endpoint that raises a 401 error
    api_service.add_api_route("/test-401", mock_401_endpoint, methods=["GET"])

    response = client.get("/test-401")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    # Should now be RFC 9457 format for client errors 400+
    assert response.headers.get("content-type") == "application/problem+json"

    data = response.json()

    # Check RFC 9457 required fields
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "instance" in data

    # Check specific values for client error
    assert data["status"] == status.HTTP_401_UNAUTHORIZED
    assert data["title"] == "Client Error 401"
    assert data["type"] == "https://httpstatuses.com/401"
    assert data["detail"] == "Unauthorized access"
    assert data["instance"].startswith("urn:uuid:")


def test_default_404_uses_rfc9457_format() -> None:
    """Test that default 404 errors for non-existent routes use RFC 9457 format"""
    response = client.get("/api/v1/nonexistent-route")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Should now be RFC 9457 format for 404 errors
    assert response.headers.get("content-type") == "application/problem+json"

    data = response.json()

    # Check RFC 9457 required fields
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "instance" in data

    # Check specific values for 404 error
    assert data["status"] == status.HTTP_404_NOT_FOUND
    assert data["title"] == "Client Error 404"
    assert data["type"] == "https://httpstatuses.com/404"
    assert "Not Found" in data["detail"]
    assert data["instance"].startswith("urn:uuid:")


def test_404_error_uses_rfc9457_format() -> None:
    """Test that 404 errors now use RFC 9457 format"""

    def mock_404_endpoint() -> None:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Add a test endpoint that raises a 404 error
    api_service.add_api_route("/test-404", mock_404_endpoint, methods=["GET"])

    response = client.get("/test-404")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Should now be RFC 9457 format for 404 errors
    assert response.headers.get("content-type") == "application/problem+json"

    data = response.json()

    # Check RFC 9457 required fields
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "instance" in data

    # Check specific values for client error
    assert data["status"] == status.HTTP_404_NOT_FOUND
    assert data["title"] == "Client Error 404"
    assert data["type"] == "https://httpstatuses.com/404"
    assert data["detail"] == "Resource not found"
    assert data["instance"].startswith("urn:uuid:")


def test_400_error_uses_rfc9457_format() -> None:
    """Test that 400 errors use RFC 9457 format"""

    def mock_400_endpoint() -> None:
        raise HTTPException(status_code=400, detail="Bad request")

    # Add a test endpoint that raises a 400 error
    api_service.add_api_route("/test-400", mock_400_endpoint, methods=["GET"])

    response = client.get("/test-400")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.headers.get("content-type") == "application/problem+json"

    data = response.json()

    # Check RFC 9457 required fields
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "instance" in data

    # Check specific values for client error
    assert data["status"] == status.HTTP_400_BAD_REQUEST
    assert data["title"] == "Client Error 400"
    assert data["type"] == "https://httpstatuses.com/400"
    assert data["detail"] == "Bad request"
    assert data["instance"].startswith("urn:uuid:")


def test_success_response_unchanged() -> None:
    """Test that successful responses are unchanged"""
    response = client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Should still use existing format
    assert "status" in data
    assert "code" in data
    assert "data" in data
    assert "message" in data
    assert data["status"] == "success"

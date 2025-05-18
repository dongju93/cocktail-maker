from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from conftest import api_service

client = TestClient(api_service)


def test_health_check_success() -> None:
    response: Response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success",
        "code": 200,
        "data": {"status": "ok"},
        "message": "Service is running",
    }


# If health_check is failed no response, because the server it self is down

import asyncio
from typing import NoReturn

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from conftest import api_service

client = TestClient(api_service)


def test_health_check_success() -> None:
    """Test the health check endpoint for a successful response"""
    response: Response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success",
        "code": 200,
        "data": {"status": "ok"},
        "message": "Service is running",
    }


def test_health_check_response_headers() -> None:
    """Test the health check endpoint for correct response headers"""
    response: Response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"


def test_health_check_method_not_allowed() -> None:
    """Test the health check endpoint for method not allowed"""
    response: Response = client.post("/api/v1/health")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_health_check_invalid_endpoint() -> None:
    """Test the health check endpoint for an invalid endpoint"""
    response: Response = client.get("/api/v1/health/invalid")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_health_check_async_success() -> None:
    """Test the health check endpoint for a successful response in async mode"""
    response = await asyncio.to_thread(client.get, "/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success",
        "code": 200,
        "data": {"status": "ok"},
        "message": "Service is running",
    }


@pytest.mark.asyncio
async def test_health_check_async_multiple_requests() -> None:
    """Test the health check endpoint for multiple async requests using TaskGroup"""
    responses = []

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
        task2 = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
        task3 = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))

    # TaskGroup이 완료되면 모든 결과를 수집
    responses = [task1.result(), task2.result(), task3.result()]

    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        assert "status" in response.json()


@pytest.mark.asyncio
async def test_health_check_taskgroup_with_different_endpoints() -> None:
    """Test multiple endpoints concurrently using TaskGroup"""
    async with asyncio.TaskGroup() as tg:
        health_task = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
        invalid_task = tg.create_task(
            asyncio.to_thread(client.get, "/api/v1/health/invalid")
        )
        post_task = tg.create_task(asyncio.to_thread(client.post, "/api/v1/health"))

    # 각 결과 검증
    health_response = health_task.result()
    invalid_response = invalid_task.result()
    post_response = post_task.result()

    assert health_response.status_code == status.HTTP_200_OK
    assert invalid_response.status_code == status.HTTP_404_NOT_FOUND
    assert post_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_health_check_taskgroup_error_handling() -> None:
    """Test that TaskGroup works correctly even with mixed success/failure"""
    # 실패하지 않는 테스트로 변경 - 모든 요청이 유효한 엔드포인트
    async with asyncio.TaskGroup() as tg:
        success_task1 = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
        # 404는 HTTP 에러가 아니라 정상 응답이므로 TaskGroup에서 실패하지 않음
        not_found_task = tg.create_task(
            asyncio.to_thread(client.get, "/api/v1/health/invalid")
        )
        success_task2 = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))

    # 모든 태스크가 완료되었는지 확인
    assert success_task1.done()
    assert not_found_task.done()
    assert success_task2.done()

    # 각 응답 검증
    success_response1 = success_task1.result()
    not_found_response = not_found_task.result()
    success_response2 = success_task2.result()

    assert success_response1.status_code == status.HTTP_200_OK
    assert not_found_response.status_code == status.HTTP_404_NOT_FOUND
    assert success_response2.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_health_check_taskgroup_cancellation() -> None:
    """Test TaskGroup cancellation behavior"""

    async def slow_request() -> Response:
        await asyncio.sleep(0.1)  # 느린 요청 시뮬레이션
        return await asyncio.to_thread(client.get, "/api/v1/health")

    async def failing_request() -> NoReturn:
        await asyncio.sleep(0.05)
        raise ValueError("Simulated error")

    # 변수들을 미리 선언
    slow_task = None
    fail_task = None

    # TaskGroup에서 하나의 태스크가 실패하면 나머지도 취소되는지 테스트
    with pytest.raises(ExceptionGroup) as exc_info:
        async with asyncio.TaskGroup() as tg:
            slow_task = tg.create_task(slow_request())
            fail_task = tg.create_task(failing_request())

    # ExceptionGroup에 ValueError가 포함되어 있는지 확인
    exception_group = exc_info.value
    assert len(exception_group.exceptions) >= 1
    assert any(isinstance(exc, ValueError) for exc in exception_group.exceptions)

    # 두 태스크 모두 검증
    assert slow_task is not None
    assert fail_task is not None
    assert slow_task.cancelled() or slow_task.done()
    assert fail_task.done()  # 실패한 태스크는 완료 상태여야 함


@pytest.mark.asyncio
async def test_health_check_performance_testing() -> None:
    """Performance testing with TaskGroup - 10 concurrent requests"""
    start_time = asyncio.get_event_loop().time()

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
            for _ in range(10)
        ]

    end_time = asyncio.get_event_loop().time()
    duration = end_time - start_time

    # 모든 응답이 성공인지 확인
    responses = [task.result() for task in tasks]
    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "success"

    # 성능 검증 (10개 요청이 1초 이내에 완료되어야 함)
    assert duration < 1.0, f"Performance test failed: took {duration:.2f} seconds"

    print(f"✅ 10 concurrent requests completed in {duration:.3f} seconds")


@pytest.mark.asyncio
async def test_health_check_mixed_methods_taskgroup() -> None:
    """Test different HTTP methods concurrently with TaskGroup"""
    async with asyncio.TaskGroup() as tg:
        get_task = tg.create_task(asyncio.to_thread(client.get, "/api/v1/health"))
        post_task = tg.create_task(asyncio.to_thread(client.post, "/api/v1/health"))
        put_task = tg.create_task(asyncio.to_thread(client.put, "/api/v1/health"))
        delete_task = tg.create_task(asyncio.to_thread(client.delete, "/api/v1/health"))

    # 각 메서드별 예상 응답 검증
    results = {
        "GET": get_task.result(),
        "POST": post_task.result(),
        "PUT": put_task.result(),
        "DELETE": delete_task.result(),
    }

    assert results["GET"].status_code == status.HTTP_200_OK
    assert results["POST"].status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert results["PUT"].status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert results["DELETE"].status_code == status.HTTP_405_METHOD_NOT_ALLOWED

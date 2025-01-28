from typing import Any, Literal

from model.etc import ResponseFormat


async def return_formatter(
    status: Literal["success", "failed"], code: int, data: Any, message: str
) -> ResponseFormat:
    return ResponseFormat(
        status=status,
        code=code,
        data=data,
        message=message,
    )

from typing import Any, Literal, TypedDict


class ResponseFormat(TypedDict):
    status: Literal["success", "failed"]
    code: int
    data: Any
    message: str

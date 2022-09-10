from typing import Any

from app.common.errors import ServiceError
from app.common.json import preprocess_json
from fastapi.responses import ORJSONResponse


def success(content: Any, status_code: int = 200, headers: dict | None = None) -> ORJSONResponse:
    content = preprocess_json(content)
    data = {"status": "success", "data": content}
    return ORJSONResponse(data, status_code, headers)


# TODO: make this more clear on the business case?


def failure(error: ServiceError, message: str, status_code: int = 400,
            headers: dict | None = None) -> ORJSONResponse:
    data = {"status": "error", "error": error, "message": message}
    return ORJSONResponse(data, status_code, headers)

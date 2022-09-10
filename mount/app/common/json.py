import uuid
from typing import Any

from asyncpg.pgproto import pgproto
from pydantic import BaseModel


def preprocess_json(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return preprocess_json(data.dict())
    elif isinstance(data, dict):
        return {k: preprocess_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [preprocess_json(v) for v in data]
    elif isinstance(data, (uuid.UUID, pgproto.UUID)):
        return str(data)
    else:
        return data

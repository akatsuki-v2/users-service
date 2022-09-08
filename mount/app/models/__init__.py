from __future__ import annotations

from enum import Enum

from pydantic import BaseModel as _pydantic_BaseModel


class Status(str, Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    DELETED = 'deleted'


class BaseModel(_pydantic_BaseModel):
    class Config:
        anystr_strip_whitespace = True

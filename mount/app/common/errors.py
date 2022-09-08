from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    ACCOUNTS_CANNOT_CREATE = 'accounts.cannot_create'

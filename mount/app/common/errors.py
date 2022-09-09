from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    ACCOUNTS_CANNOT_CREATE = 'accounts.cannot_create'
    ACCOUNTS_NOT_FOUND = 'accounts.not_found'

    CREDENTIALS_CANNOT_CREATE = 'credentials.cannot_create'
    CREDENTIALS_NOT_FOUND = 'credentials.not_found'

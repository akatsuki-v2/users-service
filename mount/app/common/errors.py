from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    ACCOUNTS_CANNOT_CREATE = 'accounts.cannot_create'
    ACCOUNTS_NOT_FOUND = 'accounts.not_found'
    ACCOUNTS_EMAIL_ADDRESS_EXISTS = 'accounts.email_address_exists'
    ACCOUNTS_USERNAME_EXISTS = 'accounts.username_exists'

    CREDENTIALS_CANNOT_CREATE = 'credentials.cannot_create'
    CREDENTIALS_NOT_FOUND = 'credentials.not_found'

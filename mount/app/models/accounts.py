from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Mapping
from uuid import UUID

from . import BaseModel
from . import Status


class BaseAccount(BaseModel):
    account_id: UUID
    username: str
    safe_username: str
    email_address: str
    country: str  # iso-3166-1 alpha-2


class Account(BaseAccount):
    rec_id: int
    status: Status
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> BaseAccount:
        return cls(
            rec_id=mapping["rec_id"],
            account_id=mapping["account_id"],
            username=mapping["username"],
            safe_username=mapping["safe_username"],
            email_address=mapping["email_address"],
            country=mapping["country"],
            status=mapping["status"],
            created_at=mapping["created_at"],
            updated_at=mapping["updated_at"],
        )


class AccountInput(BaseAccount):
    password: str


class AccountUpdate(BaseModel):
    username: str | None
    email_address: str | None
    country: str | None  # iso-3166-1 alpha-2

    # private endpoint feature
    # not to be exposed to users
    status: Status

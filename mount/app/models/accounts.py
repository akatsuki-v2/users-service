from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Mapping
from uuid import UUID

from . import BaseModel
from . import Status


# NOTE: the `country` field is iso-3166-1 alpha-2


class SignupForm(BaseModel):
    username: str
    password: str
    email_address: str
    country: str


class Account(BaseModel):
    rec_id: int
    account_id: UUID
    username: str
    safe_username: str  # NOTE: generated column
    email_address: str
    country: str
    created_at: datetime
    updated_at: datetime
    status: Status

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> Account:
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


class AccountUpdate(BaseModel):
    username: str | None
    email_address: str | None
    country: str | None

    # private endpoint feature
    # not to be exposed to users
    status: Status

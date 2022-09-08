from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Mapping
from uuid import UUID

from . import BaseModel
from . import Status


class Account(BaseModel):
    rec_id: int
    account_id: UUID
    username: str
    safe_username: str
    email_address: str
    country: str
    status: Status
    created_at: datetime
    updated_at: datetime

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

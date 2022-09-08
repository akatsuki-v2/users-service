from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Mapping
from uuid import UUID

from . import BaseModel


class Session(BaseModel):
    session_id: UUID
    account_id: UUID
    user_agent: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> Session:
        return cls(
            session_id=mapping["session_id"],
            account_id=mapping["account_id"],
            user_agent=mapping["user_agent"],
            expires_at=mapping["expires_at"],
            created_at=mapping["created_at"],
            updated_at=mapping["updated_at"],
        )

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Mapping
from uuid import UUID

from app.common import json
from app.common.context import Context

SESSION_EXPIRY = 3600  # 1h


def create_session_key(session_id: UUID) -> str:
    return f"users:sessions:{session_id}"

# TODO: is my usage of setex correct?
# i'm technically desyncing from the expires_at var


class SessionsRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, session_id: UUID, account_id: int,
                     user_agent: str) -> Mapping[str, Any]:
        now = datetime.now()
        expires_at = now + timedelta(seconds=SESSION_EXPIRY)
        session = {
            "session_id": session_id,
            "account_id": account_id,
            "user_agent": user_agent,
            "expires_at": expires_at,
            "created_at": now,
            "updated_at": now,
        }
        await self.ctx.redis.setex(create_session_key(session_id),
                                   SESSION_EXPIRY, json.dumps(session))
        return session

    async def fetch_one(self, session_id: UUID) -> Mapping[str, Any] | None:
        session = await self.ctx.redis.get(create_session_key(session_id))
        if session is None:
            return None
        return json.loads(session)

    # TODO: fetch all? (with filters)

    async def partial_update(self, session_id: UUID, **kwargs: Any) -> Mapping[str, Any] | None:
        session = await self.fetch_one(session_id)
        if session is None:
            return None

        if not kwargs:
            return session

        session = dict(session)
        session.update(kwargs)
        session["updated_at"] = datetime.now()

        await self.ctx.redis.set(create_session_key(session_id), json.dumps(session))

        if expires_at := kwargs.get("expires_at"):
            await self.ctx.redis.expireat(create_session_key(session_id), expires_at)

        return session

    async def delete(self, session_id: UUID) -> Mapping[str, Any] | None:
        session_key = create_session_key(session_id)

        session = await self.ctx.redis.get(session_key)
        if session is None:
            return None

        # TODO: should we be actually deleting?
        await self.ctx.redis.delete(session_key)

        return session

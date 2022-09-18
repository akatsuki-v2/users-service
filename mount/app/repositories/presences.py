from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Mapping
from uuid import UUID

from app.common import json
from app.common.context import Context


def create_presence_key(session_id: UUID) -> str:
    return f"users:sessions:{session_id}:presence"


class PresencesRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     session_id: UUID,
                     #  account_id: int,
                     game_mode: int,
                     country_code: str,
                     privileges: int,
                     latitude: float,
                     longitude: float,
                     action: int,  # TODO: enum
                     info_text: str,
                     map_md5: str,
                     map_id: int,
                     mods: int,
                     expires_at: datetime) -> Mapping[str, Any]:
        now = datetime.now()
        session = {
            "session_id": session_id,
            # "account_id": account_id,
            "game_mode": game_mode,
            "country_code": country_code,
            "privileges": privileges,
            "latitude": latitude,
            "longitude": longitude,
            "action": action,
            "info_text": info_text,
            "map_md5": map_md5,
            "map_id": map_id,
            "mods": mods,
            "created_at": now,
            "updated_at": now,
        }
        await self.ctx.redis.set(create_presence_key(session_id),
                                 json.dumps(session))
        await self.ctx.redis.expireat(create_presence_key(session_id),
                                      expires_at)
        return session

    async def fetch_one(self, session_id: UUID) -> Mapping[str, Any] | None:
        session = await self.ctx.redis.get(create_presence_key(session_id))
        if session is None:
            return None
        return json.loads(session)

    async def fetch_all(self) -> list[Mapping[str, Any]]:
        keys = await self.ctx.redis.keys("users:sessions:*:presence")
        sessions = await self.ctx.redis.mget(*keys)
        return [json.loads(session) for session in sessions]

    async def partial_update(self, session_id: UUID, **kwargs: Any) -> Mapping[str, Any] | None:
        presence = await self.fetch_one(session_id)
        if presence is None:
            return None

        if not kwargs:
            return presence

        presence = dict(presence)
        presence.update(kwargs)
        presence["updated_at"] = datetime.now()

        await self.ctx.redis.set(create_presence_key(session_id),
                                 json.dumps(presence))

        if expires_at := kwargs.get("expires_at"):  # maybe a bit weird?
            await self.ctx.redis.expireat(create_presence_key(session_id),
                                          expires_at)

        return presence

    async def delete(self, session_id: UUID) -> Mapping[str, Any] | None:
        session = await self.fetch_one(session_id)
        if session is None:
            return None

        await self.ctx.redis.delete(create_presence_key(session_id))

        return session

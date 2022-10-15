from datetime import datetime
from typing import Any
from uuid import UUID

from app.common import json
from app.common.context import Context


def create_spectator_key(host_session_id: UUID) -> str:
    return f"users:spectators:{host_session_id}"


def create_spectating_key(spectator_session_id: UUID) -> str:
    return f"users:spectating:{spectator_session_id}"


class SpectatorsRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, host_session_id: UUID, session_id: UUID,
                     account_id: int) -> dict[str, Any]:
        now = datetime.now()
        spectator = {
            "session_id": session_id,
            "account_id": account_id,
            "created_at": now,
        }
        await self.ctx.redis.sadd(create_spectator_key(host_session_id),
                                  json.dumps(spectator))
        await self.ctx.redis.set(create_spectating_key(session_id),
                                 str(host_session_id))
        return spectator

    # TODO: make sure it's possible to *actually* fetch *all* spectators easily
    async def fetch_all(self, host_session_id: UUID,
                        session_id: UUID | None = None,
                        account_id: int | None = None,
                        page: int = 1, page_size: int = 10) -> list[dict[str, Any]]:
        spectator_key = create_spectator_key(host_session_id)

        if page > 1:
            cursor, elements = await self.ctx.redis.sscan(name=spectator_key,
                                                          cursor=0,
                                                          count=(page - 1) * page_size)
        else:
            cursor = None

        spectators = []
        while cursor != 0:
            cursor, elements = await self.ctx.redis.sscan(name=spectator_key,
                                                          cursor=cursor or 0,
                                                          count=page_size)

            for element in elements:
                spectator = json.loads(element)

                if session_id is not None and spectator["session_id"] != session_id:
                    continue

                if account_id is not None and spectator["account_id"] != account_id:
                    continue

                spectators.append(spectator)

        return spectators

    async def get_host(self, spectator_session_id: UUID) -> str | None:
        host_session_id: bytes | None = await self.ctx.redis.get(
            create_spectating_key(spectator_session_id))
        if host_session_id is None:
            return None
        return host_session_id.decode()

    async def delete(self, host_session_id: UUID, spectator_session_id: UUID
                     ) -> dict[str, Any] | None:
        # TODO: this is pretty hacky/wrong
        spectators = await self.fetch_all(host_session_id,
                                          session_id=spectator_session_id)
        if len(spectators) == 0:
            return None

        spectator = spectators[0]

        await self.ctx.redis.srem(create_spectator_key(host_session_id),
                                  str(spectator_session_id))

        await self.ctx.redis.delete(create_spectating_key(spectator_session_id),
                                    str(host_session_id))

        return spectator

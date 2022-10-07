from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from app.common import json
from app.common.context import Context


def create_queued_packets_key(session_id: str | UUID) -> str:
    return f"users:queued-packets:{session_id}"


# TODO: packet expiry?
class QueuedPacketsRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def enqueue(self, session_id: UUID, data: bytes) -> dict[str, Any]:
        now = datetime.now()
        packet = {
            "session_id": session_id,  # overkill?
            "data": list(data),
            "created_at": now,
        }
        queue_size = await self.ctx.redis.rpush(create_queued_packets_key(session_id),
                                                json.dumps(packet))
        return packet

    async def dequeue_one(self, session_id: UUID) -> dict[str, Any] | None:
        data = await self.ctx.redis.lpop(create_queued_packets_key(session_id))
        if data is None:
            return None

        return json.loads(data)

    async def dequeue_all(self, session_id: UUID) -> list[dict[str, Any]]:
        data = await self.ctx.redis.lrange(create_queued_packets_key(session_id),
                                           0, -1)
        if data is None:
            return []

        await self.ctx.redis.delete(create_queued_packets_key(session_id))

        return data
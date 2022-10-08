from typing import Any
from uuid import UUID

from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.queued_packets import QueuedPacketsRepo


async def enqueue(ctx: Context, session_id: UUID, data: list[int]
                  ) -> dict[str, Any] | ServiceError:
    repo = QueuedPacketsRepo(ctx)

    packet = await repo.enqueue(session_id, data)
    return packet


async def dequeue_one(ctx: Context, session_id: UUID) -> dict[str, Any] | ServiceError:
    repo = QueuedPacketsRepo(ctx)

    packet = await repo.dequeue_one(session_id)
    if not packet:
        return ServiceError.QUEUED_PACKETS_NONE_REMAINING

    return packet


async def dequeue_all(ctx: Context, session_id: UUID) -> list[dict[str, Any]] | ServiceError:
    repo = QueuedPacketsRepo(ctx)

    packets = await repo.dequeue_all(session_id)
    return packets

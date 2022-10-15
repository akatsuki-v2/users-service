from typing import Any
from uuid import UUID

from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.spectators import SpectatorsRepo


async def create(ctx: Context, host_session_id: UUID,
                 session_id: UUID, account_id: int) -> dict[str, Any] | ServiceError:
    repo = SpectatorsRepo(ctx)

    spectator = await repo.create(host_session_id, session_id, account_id)
    if spectator is None:
        return ServiceError.SPECTATORS_CANNOT_CREATE

    return spectator


async def fetch_all(ctx: Context, host_session_id: UUID) -> list[dict[str, Any]]:
    repo = SpectatorsRepo(ctx)

    spectators = await repo.fetch_all(host_session_id)

    return spectators


async def get_host(ctx: Context, session_id: UUID) -> str | ServiceError:
    repo = SpectatorsRepo(ctx)

    host = await repo.get_host(session_id)
    if host is None:
        return ServiceError.SPECTATOR_HOST_NOT_FOUND

    return host


async def delete(ctx: Context, host_session_id: UUID,
                 session_id: UUID) -> dict[str, Any] | ServiceError:
    repo = SpectatorsRepo(ctx)

    spectator = await repo.delete(host_session_id, session_id)
    if spectator is None:
        return ServiceError.SPECTATORS_NOT_FOUND

    return spectator

from uuid import UUID

from app.common.context import Context
from app.repositories.spectators import SpectatorsRepo


async def create(ctx: Context, host_session_id: UUID,
                 spectator_session_id: UUID) -> None:
    repo = SpectatorsRepo(ctx)
    await repo.create(host_session_id, spectator_session_id)


async def fetch_all(ctx: Context, host_session_id: UUID) -> list[str]:
    repo = SpectatorsRepo(ctx)
    return await repo.fetch_all(host_session_id)


async def delete(ctx: Context, host_session_id: UUID,
                 spectator_session_id: UUID) -> None:
    repo = SpectatorsRepo(ctx)
    await repo.delete(host_session_id, spectator_session_id)

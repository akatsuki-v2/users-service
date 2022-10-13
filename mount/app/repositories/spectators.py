from uuid import UUID

from app.common.context import Context


def create_spectator_key(host_session_id: UUID) -> str:
    return f"users:spectators:{host_session_id}"


class SpectatorsRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, host_session_id: UUID, spectator_session_id: UUID) -> None:
        await self.ctx.redis.sadd(create_spectator_key(host_session_id),
                                  str(spectator_session_id))

    # TODO: make sure it's possible to *actually* fetch *all* spectators easily
    async def fetch_all(self, host_session_id: UUID,
                        page: int = 1, page_size: int = 10) -> list[str]:
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
            spectators.extend([e.decode() for e in elements])

        return spectators

    async def delete(self, host_session_id: UUID, spectator_session_id: UUID) -> None:
        await self.ctx.redis.srem(create_spectator_key(host_session_id),
                                  str(spectator_session_id))

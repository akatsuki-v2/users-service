from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any
from uuid import UUID

from app.common import logging
from app.common.context import Context
from app.common.errors import ServiceError
from app.models.presences import PresenceUpdate
from app.repositories.presences import PresencesRepo
from app.repositories.sessions import SessionsRepo


async def create(ctx: Context,
                 session_id: UUID,
                 game_mode: int,
                 country_code: str,
                 privileges: int,
                 latitude: float,
                 longitude: float,
                 action: int,
                 info_text: str,
                 map_md5: str,
                 map_id: int,
                 mods: int) -> Mapping[str, Any] | ServiceError:
    p_repo = PresencesRepo(ctx)
    s_repo = SessionsRepo(ctx)

    session = await s_repo.fetch_one(session_id)
    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    try:
        presence = await p_repo.create(session_id=session_id,
                                       game_mode=game_mode,
                                       country_code=country_code,
                                       privileges=privileges,
                                       latitude=latitude,
                                       longitude=longitude,
                                       action=action,
                                       info_text=info_text,
                                       map_md5=map_md5,
                                       map_id=map_id,
                                       mods=mods,
                                       expires_at=session["expires_at"])
    except Exception as exc:
        logging.error("Unable to create presence:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.PRESENCES_CANNOT_CREATE

    return presence


async def fetch_one(ctx: Context, session_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = PresencesRepo(ctx)

    presence = await repo.fetch_one(session_id)
    if presence is None:
        return ServiceError.PRESENCES_NOT_FOUND

    return presence


async def partial_update(ctx: Context, session_id: UUID, **kwargs: Any | None
                         ) -> Mapping[str, Any] | ServiceError:
    repo = PresencesRepo(ctx)

    updates = {
        field: value
        for field in PresenceUpdate.__fields__
        if (value := kwargs.get(field)) is not None
    }

    presence = await repo.partial_update(session_id=session_id, **updates)
    if presence is None:
        return ServiceError.PRESENCES_NOT_FOUND

    return presence


async def delete(ctx: Context, session_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = PresencesRepo(ctx)

    presence = await repo.delete(session_id)
    if presence is None:
        return ServiceError.PRESENCES_NOT_FOUND

    return presence

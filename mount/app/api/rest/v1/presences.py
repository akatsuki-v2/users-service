from __future__ import annotations

from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.presences import Presence
from app.models.presences import PresenceInput
from app.models.presences import PresenceUpdate
from app.usecases import presences
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/presences", response_model=Success[Presence])
async def create_presence(args: PresenceInput,
                          ctx: RequestContext = Depends()):
    data = await presences.create(ctx, session_id=args.session_id,
                                  game_mode=args.game_mode,
                                  account_id=args.account_id,
                                  username=args.username,
                                  country_code=args.country_code,
                                  privileges=args.privileges,
                                  latitude=args.latitude,
                                  longitude=args.longitude,
                                  action=args.action,
                                  info_text=args.info_text,
                                  map_md5=args.map_md5,
                                  map_id=args.map_id,
                                  mods=args.mods,
                                  osu_version=args.osu_version,
                                  utc_offset=args.utc_offset,
                                  display_city=args.display_city,
                                  pm_private=args.pm_private)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create presence")

    resp = Presence.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/presences/{session_id}", response_model=Success[Presence])
async def fetch_one(session_id: UUID, ctx: RequestContext = Depends()):
    data = await presences.fetch_one(ctx, session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch presence")

    resp = Presence.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/presences", response_model=Success[list[Presence]])
async def fetch_all(game_mode: int | None = None,
                    account_id: int | None = None,
                    username: str | None = None,
                    country_code: str | None = None,
                    # privileges: int | None = None,

                    osu_version: str | None = None,
                    utc_offset: int | None = None,
                    display_city: bool | None = None,
                    pm_private: bool | None = None,
                    ctx: RequestContext = Depends()):
    data = await presences.fetch_all(ctx, game_mode=game_mode,
                                     account_id=account_id,
                                     username=username,
                                     country_code=country_code,
                                     # privileges=privileges,

                                     osu_version=osu_version,
                                     utc_offset=utc_offset,
                                     display_city=display_city,
                                     pm_private=pm_private)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch presences")

    resp = [Presence.from_mapping(rec) for rec in data]
    return responses.success(resp)


@router.patch("/v1/presences/{session_id}", response_model=Success[Presence])
async def partial_update_presence(session_id: UUID, args: PresenceUpdate,
                                  ctx: RequestContext = Depends()):
    data = await presences.partial_update(ctx, session_id,
                                          game_mode=args.game_mode,
                                          country_code=args.country_code,
                                          privileges=args.privileges,
                                          latitude=args.latitude,
                                          longitude=args.longitude,
                                          action=args.action,
                                          info_text=args.info_text,
                                          map_md5=args.map_md5,
                                          map_id=args.map_id,
                                          mods=args.mods,
                                          osu_version=args.osu_version,
                                          utc_offset=args.utc_offset,
                                          display_city=args.display_city,
                                          pm_private=args.pm_private)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update presence")

    resp = Presence.from_mapping(data)
    return responses.success(resp)


@router.delete("/v1/presences/{session_id}", response_model=Success[Presence])
async def delete_presence(session_id: UUID, ctx: RequestContext = Depends()):
    data = await presences.delete(ctx, session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete presence")

    resp = Presence.from_mapping(data)
    return responses.success(resp)

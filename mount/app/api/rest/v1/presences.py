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
    data = await presences.create(ctx, **args.dict())
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


@router.patch("/v1/presences/{session_id}", response_model=Success[Presence])
async def partial_update_presence(session_id: UUID, args: PresenceUpdate,
                                  ctx: RequestContext = Depends()):
    data = await presences.partial_update(ctx, session_id, **args.dict())
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

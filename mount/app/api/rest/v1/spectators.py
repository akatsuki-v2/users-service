from __future__ import annotations

from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.spectators import Spectator
from app.models.spectators import SpectatorInput
from app.usecases import spectators
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/sessions/{host_session_id}/spectators",
             response_model=Success[Spectator])
async def create(host_session_id: UUID, args: SpectatorInput,
                 ctx: RequestContext = Depends()):
    data = await spectators.create(ctx, host_session_id,
                                   args.session_id,
                                   args.account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create spectator")

    resp = Spectator.from_mapping(data)
    return responses.success(resp)


@router.delete("/v1/sessions/{host_session_id}/spectators/{spectator_session_id}",
               response_model=Success[Spectator])
async def delete(host_session_id: UUID, spectator_session_id: UUID,
                 ctx: RequestContext = Depends()):
    data = await spectators.delete(ctx, host_session_id, spectator_session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete spectator")

    resp = Spectator.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/sessions/{host_session_id}/spectators",
            response_model=Success[list[str]])
async def fetch_all(host_session_id: UUID, ctx: RequestContext = Depends()):
    data = await spectators.fetch_all(ctx, host_session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get spectators")

    resp = [Spectator.from_mapping(rec) for rec in data]
    return responses.success(resp)


# TODO: this is pretty weird
@router.get("/v1/sessions/{spectator_session_id}/spectating",
            response_model=Success[UUID])
async def get_host(spectator_session_id: UUID, ctx: RequestContext = Depends()):
    data = await spectators.get_host(ctx, spectator_session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get host")

    resp = UUID(data)
    return responses.success(resp)

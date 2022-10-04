from __future__ import annotations

from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.queued_packets import EnqueuePacket
from app.models.queued_packets import QueuedPacket
from app.usecases import queued_packets
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/sessions/{session_id}/queued-packets",
             response_model=Success[QueuedPacket])
async def enqueue(session_id: UUID, args: EnqueuePacket,
                  ctx: RequestContext = Depends()):
    data = await queued_packets.enqueue(ctx, session_id, data=args.data)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to enqueue packet")

    resp = QueuedPacket.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/sessions/{session_id}/queued-packets",
            response_model=Success[list[QueuedPacket]])
async def dequeue_all(session_id: UUID, ctx: RequestContext = Depends()):
    data = await queued_packets.dequeue_all(ctx, session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to dequeue packets")

    resp = [QueuedPacket.from_mapping(rec) for rec in data]
    return responses.success(resp)

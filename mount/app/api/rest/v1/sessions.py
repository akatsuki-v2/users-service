from __future__ import annotations

from app.api.rest.context import RequestContext
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-11
@router.post("/v1/sessions")
async def login(ctx: RequestContext = Depends()):
    ...


# https://osuakatsuki.atlassian.net/browse/V2-13
@router.delete("/v1/sessions/{session_id}")
async def logout(session_id: str, ctx: RequestContext = Depends()):
    ...


# TODO: not sure if this is needed
# https://osuakatsuki.atlassian.net/browse/V2-12
@router.post("/v1/sessions/{session_id}/refresh")
async def refresh_session(session_id: str, ctx: RequestContext = Depends()):
    ...

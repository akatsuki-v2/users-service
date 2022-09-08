from __future__ import annotations

from app.api.rest.context import RequestContext
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-10
@router.post("/v1/accounts")
async def create_account(ctx: RequestContext = Depends()):
    ...


# https://osuakatsuki.atlassian.net/browse/V2-58
@router.get("/v1/accounts/{account_id}")
async def get_account(account_id: str, ctx: RequestContext = Depends()):
    ...


# https://osuakatsuki.atlassian.net/browse/V2-59
@router.patch("/v1/accounts/{account_id}")
async def partial_update_account(account_id: str, ctx: RequestContext = Depends()):
    ...

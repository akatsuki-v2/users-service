from __future__ import annotations

from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.models.accounts import Account
from app.models.accounts import AccountUpdate
from app.models.accounts import SignupForm
from app.usecases import accounts
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-10
@router.post("/v1/accounts", response_model=Account)
async def sign_up(args: SignupForm, ctx: RequestContext = Depends()):
    data = await accounts.sign_up(ctx,
                                  args.username,
                                  args.password,
                                  args.email_address,
                                  args.country)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to signup for account")

    resp = Account.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-58
@router.get("/v1/accounts/{account_id}", response_model=Account)
async def get_account(account_id: UUID, ctx: RequestContext = Depends()):
    data = await accounts.fetch_one(ctx, account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch account")

    resp = Account.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-59
@router.patch("/v1/accounts/{account_id}", response_model=Account)
async def partial_update_account(account_id: UUID, args: AccountUpdate,
                                 ctx: RequestContext = Depends()):
    data = await accounts.partial_update(ctx, account_id, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update account")

    resp = Account.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-44
@router.delete("v1/accounts/{account_id}", response_model=Account)
async def delete_account(account_id: UUID, ctx: RequestContext = Depends()):
    data = await accounts.delete(ctx, account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete account")

    resp = Account.from_mapping(data)
    return responses.success(resp)
